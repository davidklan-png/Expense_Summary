"""Command-line interface for Saison Transform.

Provides the main entry point and CLI commands for the application.
Uses Typer for robust CLI architecture with subcommands.
"""

import sys
import warnings
from pathlib import Path
from typing import Optional

import typer

from .config import Config

# Create Typer app
app = typer.Typer(
    name="saisonxform",
    help="Financial Transaction Processor - Process credit card statements and assign attendees",
    add_completion=False,
)


@app.command()
def run(
    month: list[str] = typer.Option(
        [],
        "--month",
        "-m",
        help="Process specific month(s) in YYYYMM format (repeatable). Default: latest 2 months.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force reprocessing of already-archived months",
    ),
    input_dir: Optional[Path] = typer.Option(
        None,
        "--input",
        help="Override input directory path",
    ),
    reference_dir: Optional[Path] = typer.Option(
        None,
        "--reference",
        help="Override reference directory path",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Override output directory path",
    ),
    archive_dir: Optional[Path] = typer.Option(
        None,
        "--archive",
        help="Override archive directory path",
    ),
    config_file: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to config.toml file",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose logging (with sensitive data redaction)",
    ),
) -> None:
    """Process transaction CSV files from Input directory.

    By default, processes the latest 2 months based on YYYYMM filename prefixes.
    Use --month to process specific months, --force to reprocess archived months.
    """
    import pandas as pd

    from saisonxform.io import read_csv_with_detection, write_csv_utf8_bom
    from saisonxform.month_utils import filter_files_by_months, get_archived_months, get_latest_months, has_retry_marker
    from saisonxform.reporting import generate_html_report
    from saisonxform.selectors import estimate_attendee_count, filter_relevant_transactions, sample_attendee_ids

    # Load configuration with overrides
    config = Config(config_file=config_file)

    # Apply CLI overrides with precedence logging
    precedence_log = []

    if input_dir:
        config.input_dir = input_dir
        precedence_log.append(f"input_dir: {input_dir} (from CLI --input)")
    else:
        precedence_log.append(f"input_dir: {config.input_dir} (from config)")

    if reference_dir:
        config.reference_dir = reference_dir
        precedence_log.append(f"reference_dir: {reference_dir} (from CLI --reference)")
    else:
        precedence_log.append(f"reference_dir: {config.reference_dir} (from config)")

    if output_dir:
        config.output_dir = output_dir
        precedence_log.append(f"output_dir: {output_dir} (from CLI --output)")
    else:
        precedence_log.append(f"output_dir: {config.output_dir} (from config)")

    if archive_dir:
        config.archive_dir = archive_dir
        precedence_log.append(f"archive_dir: {archive_dir} (from CLI --archive)")
    else:
        precedence_log.append(f"archive_dir: {config.archive_dir} (from config)")

    # Log configuration precedence
    if verbose:
        typer.echo("\nConfiguration Precedence:")
        for log_line in precedence_log:
            typer.echo(f"  • {log_line}")
        typer.echo()

    # TODO: Validate paths are not inside git repo (security requirement)
    # TODO: Implement archival workflow (Phase 3)

    # Load attendee reference
    namelist_path = config.reference_dir / "NameList.csv"
    if not namelist_path.exists():
        typer.echo(f"ERROR: NameList.csv not found at {namelist_path}")
        raise typer.Exit(code=1)

    attendee_ref = pd.read_csv(namelist_path, encoding="utf-8")
    available_ids = attendee_ref["ID"].astype(str).tolist()

    # Find CSV files in input directory
    all_csv_files = list(config.input_dir.glob("*.csv"))
    if not all_csv_files:
        typer.echo(f"No CSV files found in {config.input_dir}")
        raise typer.Exit(code=0)

    # Month filtering logic
    months_to_process = month  # User-specified months via --month flag
    if not months_to_process:
        # Default: process latest 2 months
        months_to_process = get_latest_months(config.input_dir, n=2)
        if months_to_process and verbose:
            typer.echo(f"No --month specified, defaulting to latest 2 months: {', '.join(months_to_process)}\n")
        elif not months_to_process:
            # No files with month prefixes found, process all files
            if verbose:
                typer.echo("No files with YYYYMM prefixes found, processing all files\n")

    # Filter files by months
    if months_to_process:
        csv_files = filter_files_by_months(all_csv_files, months_to_process)
        if verbose:
            typer.echo(f"Filtering to months: {', '.join(months_to_process)}")
            typer.echo(f"Files to process: {len(csv_files)} of {len(all_csv_files)}\n")
    else:
        csv_files = all_csv_files

    if not csv_files:
        typer.echo(f"No CSV files found matching specified months: {', '.join(months_to_process)}")
        raise typer.Exit(code=0)

    # Already-archived month detection
    if not force:
        archived_months = get_archived_months(config.archive_dir)
        if archived_months and verbose:
            typer.echo(f"Already archived months: {', '.join(sorted(archived_months))}")

        # Check if any requested months are already archived
        months_in_files = set()
        for csv_file in csv_files:
            from saisonxform.month_utils import get_month_from_filename

            file_month = get_month_from_filename(csv_file.name)
            if file_month:
                months_in_files.add(file_month)

        already_archived = months_in_files & archived_months
        if already_archived:
            # Check if they have retry markers
            months_with_retry = {m for m in already_archived if has_retry_marker(config.archive_dir, m)}
            months_without_retry = already_archived - months_with_retry

            if months_without_retry:
                typer.echo("\nERROR: The following months have already been archived:")
                for m in sorted(months_without_retry):
                    typer.echo(f"  • {m}")
                typer.echo("\nUse --force to reprocess these months.")
                raise typer.Exit(code=1)

            if months_with_retry and verbose:
                typer.echo(f"Retry markers found for: {', '.join(sorted(months_with_retry))}")
                typer.echo("These months will be reprocessed.\n")

    typer.echo(f"\nFound {len(csv_files)} CSV file(s) to process\n")

    processed_count = 0
    error_count = 0

    for csv_file in csv_files:
        try:
            typer.echo(f"Processing: {csv_file.name}")

            # Read CSV
            df, encoding = read_csv_with_detection(csv_file)
            if verbose:
                typer.echo(f"  • Detected encoding: {encoding}")
            else:
                typer.echo(f"  • Encoding: {encoding}")

            if df.empty:
                typer.echo("  • SKIPPED: Empty file")
                continue

            # TODO Phase 4: Keep ALL rows, not just filtered ones
            # Filter relevant transactions (temporarily - Phase 4 will fix this)
            relevant_df = filter_relevant_transactions(df)

            if verbose:
                typer.echo(f"  • Found {len(relevant_df)} relevant transactions (会議費/接待費)")
            else:
                typer.echo(f"  • Relevant transactions: {len(relevant_df)}")

            if len(relevant_df) == 0:
                typer.echo("  • SKIPPED: No meeting/entertainment expenses found")
                continue

            # Process each relevant transaction
            attendee_counts = []
            id_assignments = []

            for _, row in relevant_df.iterrows():
                # TODO Phase 5: Pass config parameters to estimation functions
                # Estimate attendee count
                amount = row.get("利用金額", 0)
                count = estimate_attendee_count(amount)
                attendee_counts.append(count)

                # Sample attendee IDs
                ids_dict = sample_attendee_ids(count=count, available_ids=available_ids, return_dict=True)
                id_assignments.append(ids_dict)

            # Add attendee columns to relevant transactions
            relevant_df["出席者"] = attendee_counts

            for i in range(1, 9):
                col_name = f"ID{i}"
                relevant_df[col_name] = [assignment[col_name] for assignment in id_assignments]

            # Generate output files
            output_stem = csv_file.stem
            csv_output = config.output_dir / f"{output_stem}.csv"
            html_output = config.output_dir / f"{output_stem}.html"

            # Write processed CSV
            write_csv_utf8_bom(relevant_df, csv_output, handle_duplicates=True)
            typer.echo(f"  • CSV output: {csv_output.name}")

            # Generate HTML report
            html_path = generate_html_report(
                transactions=relevant_df,
                attendee_reference=attendee_ref,
                output_path=html_output,
                source_filename=csv_file.name,
                handle_duplicates=True,
            )
            typer.echo(f"  • HTML report: {html_path.name}")

            # TODO Phase 3: Archive file after successful processing

            processed_count += 1
            typer.echo("  ✓ SUCCESS")

        except Exception as e:
            typer.echo(f"  ✗ ERROR: {e}")
            error_count += 1

        typer.echo()

    # Summary
    typer.echo("\n" + "=" * 60)
    typer.echo("Processing complete:")
    typer.echo(f"  • Processed: {processed_count}")
    typer.echo(f"  • Errors: {error_count}")
    typer.echo(f"  • Total: {len(csv_files)}")
    typer.echo("=" * 60 + "\n")

    if error_count > 0:
        raise typer.Exit(code=1)


@app.command(name="validate-config")
def validate_config(
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Validate without creating directories or files",
    ),
    config_file: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to config.toml file",
    ),
) -> None:
    """Validate configuration and check directory setup.

    Checks that all required directories exist and templates are available.
    Use --dry-run to validate without creating any directories.
    """
    typer.echo("\nValidating configuration...\n")

    try:
        # Load config
        config = Config(config_file=config_file)

        # Display configuration
        typer.echo(f"Input directory:     {config.input_dir}")
        typer.echo(f"Reference directory: {config.reference_dir}")
        typer.echo(f"Output directory:    {config.output_dir}")
        typer.echo(f"Archive directory:   {config.archive_dir}")
        typer.echo()

        # Validate directories
        typer.echo("Checking directories...")

        if dry_run:
            # In dry-run mode, just check existence without creating
            for dir_name, dir_path in [
                ("Input", config.input_dir),
                ("Reference", config.reference_dir),
                ("Output", config.output_dir),
            ]:
                if not dir_path.exists():
                    typer.echo(f"  ✗ {dir_name} directory does not exist: {dir_path}")
                else:
                    typer.echo(f"  ✓ {dir_name} directory exists")

            # Archive can be auto-created, so just note its status
            if config.archive_dir.exists():
                typer.echo("  ✓ Archive directory exists")
            else:
                typer.echo("  ℹ Archive directory will be auto-created on first use")
        else:
            # Normal mode: validate with potential directory creation
            config.validate_directories()
            typer.echo("  ✓ All required directories exist")

        typer.echo()

        # Validate templates
        typer.echo("Checking templates...")
        config.validate_templates()
        typer.echo("  ✓ All required templates exist")
        typer.echo()

        # Success message
        typer.echo("=" * 60)
        typer.echo("Configuration validation complete - SUCCESS")
        typer.echo("=" * 60)

    except FileNotFoundError as e:
        typer.echo(f"\n✗ ERROR: {e}\n")
        typer.echo("=" * 60)
        typer.echo("Configuration validation FAILED")
        typer.echo("=" * 60)
        raise typer.Exit(code=1)

    except Exception as e:
        typer.echo(f"\n✗ Unexpected error: {e}\n")
        raise typer.Exit(code=1)


def version_callback(value: bool) -> None:
    """Handle --version flag."""
    if value:
        typer.echo("saisonxform version 0.1.0")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """Saison Transform - Financial Transaction Processor."""
    # Only process if no subcommand will be invoked
    if ctx.invoked_subcommand is not None:
        return

    # Check for deprecated usage patterns
    if len(sys.argv) > 1 and not any(arg in sys.argv for arg in ["--help", "-h", "--version"]):
        deprecated_cmd = sys.argv[1]
        if deprecated_cmd == "process":
            warnings.warn(
                "The 'process' command is deprecated. Use 'run' instead.\n"
                "Example: saisonxform run\n"
                "Running 'run' command for backward compatibility...",
                DeprecationWarning,
                stacklevel=2,
            )
            # Redirect to run command
            ctx.invoke(run)
            return


def main() -> int:
    """Main entry point for the CLI.

    This function is called by the console script entry point.
    Returns exit code for compatibility with existing tests.
    """
    try:
        app()
        return 0
    except typer.Exit as e:
        return e.exit_code
    except Exception:
        return 1


# Module invocation support: python -m saisonxform.cli
if __name__ == "__main__":
    sys.exit(main())
