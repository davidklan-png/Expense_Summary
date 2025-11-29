"""Command-line interface for Saison Transform.

Provides the main entry point and CLI commands for the application.
Uses Typer for robust CLI architecture with subcommands.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer

from .config import Config


def is_inside_git_repo(path: Path) -> bool:
    """Check if a path is inside a git repository.

    Args:
        path: Path to check

    Returns:
        True if path is inside a git repository, False otherwise
    """
    try:
        # Run git rev-parse --is-inside-work-tree in the path's directory
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=path if path.is_dir() else path.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except Exception:
        return False


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
    from saisonxform.month_utils import (
        archive_file,
        create_retry_marker,
        delete_retry_marker,
        filter_files_by_months,
        get_archived_months,
        get_latest_months,
        get_month_from_filename,
        has_retry_marker,
    )
    from saisonxform.reporting import generate_html_report
    from saisonxform.selectors import estimate_attendee_count, sample_attendee_ids

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

    # Validate paths are not inside git repo (security requirement)
    paths_to_validate = [
        ("Input", config.input_dir),
        ("Reference", config.reference_dir),
        ("Output", config.output_dir),
        ("Archive", config.archive_dir),
    ]

    git_paths = []
    for name, path in paths_to_validate:
        if path.exists() and is_inside_git_repo(path):
            git_paths.append(f"{name}: {path}")

    if git_paths:
        typer.echo("\nERROR: The following directories are inside a git repository:")
        for git_path in git_paths:
            typer.echo(f"  • {git_path}")
        typer.echo("\nFor security, data directories must be outside of git repositories.")
        typer.echo("Use --input, --reference, --output, or --archive to specify different paths.")
        raise typer.Exit(code=1)

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

    # Track archival results per month
    month_results: dict[str, dict[str, list]] = {}  # month -> {succeeded: [files], failed: [(file, error)]}

    for csv_file in csv_files:
        file_month = get_month_from_filename(csv_file.name)

        try:
            typer.echo(f"Processing: {csv_file.name}")

            # Read CSV
            df, encoding, pre_header_rows = read_csv_with_detection(csv_file)
            if verbose:
                typer.echo(f"  • Detected encoding: {encoding}")
                if pre_header_rows:
                    typer.echo(f"  • Pre-header rows: {len(pre_header_rows)}")
            else:
                typer.echo(f"  • Encoding: {encoding}")

            if df.empty:
                typer.echo("  • SKIPPED: Empty file")
                continue

            # Keep ALL rows from input (including summary rows, cardholder names, etc.)
            # Only identify which rows are relevant transactions for attendee assignment
            if verbose:
                typer.echo(f"  • Total rows: {len(df)}")

            # Create mask for relevant transactions (会議費/接待費) with valid dates
            # Only these rows will get attendee data populated
            has_date = df["利用日"].notna() if "利用日" in df.columns else pd.Series([False] * len(df))
            has_subject = df["科目＆No."].notna() if "科目＆No." in df.columns else pd.Series([False] * len(df))

            # Relevant = has date AND has subject AND (会議費 OR 接待費)
            relevant_mask = has_date & has_subject & df["科目＆No."].str.contains("会議費|接待費", na=False, regex=True)
            relevant_count = relevant_mask.sum()

            if verbose:
                typer.echo(f"  • Found {relevant_count} relevant transactions (会議費/接待費)")
            else:
                typer.echo(f"  • Relevant transactions: {relevant_count}")

            # Initialize attendee columns for ALL rows (blank by default)
            df["人数"] = ""
            for i in range(1, 9):
                df[f"ID{i}"] = ""

            # Process only relevant transactions
            if relevant_count > 0:
                for idx in df[relevant_mask].index:
                    # Estimate attendee count with config parameters
                    amount = df.loc[idx, "利用金額"]

                    # Prepare amount-based parameters if configured
                    amount_brackets = None
                    cost_per_person = 3000
                    if config.amount_based_attendees:
                        amount_brackets = config.amount_based_attendees.get("brackets")
                        cost_per_person = config.amount_based_attendees.get("cost_per_person", 3000)

                    count = estimate_attendee_count(
                        amount,
                        min_attendees=config.min_attendees,
                        max_attendees=config.max_attendees,
                        amount_brackets=amount_brackets,
                        cost_per_person=cost_per_person,
                    )
                    df.loc[idx, "人数"] = count

                    # Sample attendee IDs with config weights
                    # Extract weights from config (default: 90% ID '2', 10% ID '1')
                    id_2_weight = config.primary_id_weights.get("2", 0.9)
                    id_1_weight = config.primary_id_weights.get("1", 0.1)

                    ids_result = sample_attendee_ids(
                        count=count,
                        available_ids=available_ids,
                        id_2_weight=id_2_weight,
                        id_1_weight=id_1_weight,
                        return_dict=True,
                    )
                    # Type assertion: return_dict=True guarantees dict return
                    assert isinstance(ids_result, dict)
                    for i in range(1, 9):
                        col_name = f"ID{i}"
                        df.loc[idx, col_name] = ids_result[col_name]

            # Remove unwanted columns
            columns_to_drop = ["本人・家族区分", "締前入金区分"]
            df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

            # Add new blank 備考 column at the end
            df["備考"] = ""

            # Generate output files
            output_stem = csv_file.stem
            csv_output = config.output_dir / f"{output_stem}.csv"
            html_output = config.output_dir / f"{output_stem}.html"

            # Write processed CSV (now contains ALL rows including pre-header)
            write_csv_utf8_bom(df, csv_output, handle_duplicates=True, pre_header_rows=pre_header_rows)
            typer.echo(f"  • CSV output: {csv_output.name}")

            # Generate HTML report (include ALL transactions with ALL columns)
            html_path = generate_html_report(
                transactions=df,
                attendee_reference=attendee_ref,
                output_path=html_output,
                source_filename=csv_file.name,
                pre_header_rows=pre_header_rows,
                handle_duplicates=True,
            )
            typer.echo(f"  • HTML report: {html_path.name}")

            # Archive file after successful processing
            if file_month:
                try:
                    archived_path = archive_file(csv_file, config.archive_dir, file_month)
                    if verbose:
                        typer.echo(f"  • Archived to: {archived_path}")
                    else:
                        typer.echo(f"  • Archived to: Archive/{file_month}/")

                    # Track successful archival
                    if file_month not in month_results:
                        month_results[file_month] = {"succeeded": [], "failed": []}
                    month_results[file_month]["succeeded"].append(csv_file.name)

                except Exception as archive_error:
                    typer.echo(f"  • WARNING: Failed to archive: {archive_error}")
                    # Track archival failure
                    if file_month not in month_results:
                        month_results[file_month] = {"succeeded": [], "failed": []}
                    month_results[file_month]["failed"].append((csv_file.name, str(archive_error)))

            processed_count += 1
            typer.echo("  ✓ SUCCESS")

        except Exception as e:
            typer.echo(f"  ✗ ERROR: {e}")
            error_count += 1

            # Track processing failure for retry marker
            if file_month:
                if file_month not in month_results:
                    month_results[file_month] = {"succeeded": [], "failed": []}
                month_results[file_month]["failed"].append((csv_file.name, str(e)))

        typer.echo()

    # Handle retry markers per month
    if month_results:
        for month_str, results in month_results.items():
            if results["failed"]:
                # Create retry marker for months with failures
                failed_files = [f[0] for f in results["failed"]]
                errors = [f[1] for f in results["failed"]]
                marker_path = create_retry_marker(config.archive_dir, month_str, failed_files, errors)
                if verbose:
                    typer.echo(f"Created retry marker for {month_str}: {marker_path.name}")
            elif results["succeeded"]:
                # Delete retry marker for fully successful months
                if delete_retry_marker(config.archive_dir, month_str):
                    if verbose:
                        typer.echo(f"Deleted retry marker for {month_str} (all files succeeded)")

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
        typer.echo("saisonxform version 0.2.3")
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
    """Saison Transform - Financial Transaction Processor.

    Process transaction CSV files by default. Use subcommands for other actions:
      demo             Generate sample files for testing
      validate-config  Check configuration

    Examples:
      sf                        Process latest 2 months
      sf --month 202510         Process specific month
      sf --verbose              Process with detailed logging
      sf demo                   Generate demo files
    """
    # If a subcommand is invoked, don't run the default processing
    if ctx.invoked_subcommand is not None:
        return

    # Otherwise, run the default processing (same as 'run' command)
    ctx.invoke(
        run,
        month=month,
        force=force,
        input_dir=input_dir,
        reference_dir=reference_dir,
        output_dir=output_dir,
        archive_dir=archive_dir,
        config_file=config_file,
        verbose=verbose,
    )


@app.command()
def demo(
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Directory to create demo files (default: ./saisonxform-demo)",
    ),
) -> None:
    """Generate demo files for testing the pipeline.

    Creates a demo directory with sample input files and reference data
    that can be used to test the saisonxform pipeline.
    """
    # Default output directory
    if output_dir is None:
        output_dir = Path.cwd() / "saisonxform-demo"

    # Check if directory already exists
    if output_dir.exists():
        typer.echo(f"⚠️  Directory already exists: {output_dir}")
        if not typer.confirm("Overwrite existing demo files?", default=False):
            typer.echo("Demo generation cancelled.")
            raise typer.Exit(0)

    # Create directory structure
    input_dir = output_dir / "Input"
    reference_dir = output_dir / "Reference"
    output_result_dir = output_dir / "Output"

    input_dir.mkdir(parents=True, exist_ok=True)
    reference_dir.mkdir(parents=True, exist_ok=True)
    output_result_dir.mkdir(parents=True, exist_ok=True)

    # Create sample transaction CSV
    sample_csv = input_dir / "202510_sample.csv"
    sample_csv.write_text(
        """利用日,ご利用店名及び商品名,利用金額,科目＆No.
2025-10-01,東京レストラン,15000,会議費
2025-10-05,カフェABC,5000,接待費
2025-10-10,ガソリンスタンド,8000,交通費
2025-10-15,ホテル会議室,25000,会議費
2025-10-20,居酒屋XYZ,12000,会議費・接待費
""",
        encoding="utf-8",
    )

    # Create attendee reference list
    namelist_csv = reference_dir / "NameList.csv"
    namelist_csv.write_text(
        """ID,Name,Title,Company
1,山田太郎,部長,ABC株式会社
2,佐藤花子,課長,XYZ株式会社
3,鈴木一郎,主任,DEF株式会社
4,田中美咲,係長,GHI株式会社
5,高橋健太,社員,JKL株式会社
6,伊藤誠,社員,MNO株式会社
7,渡辺和子,主任,PQR株式会社
8,小林達也,課長,STU株式会社
""",
        encoding="utf-8",
    )

    # Create config.toml with paths pointing to demo directories
    config_toml = output_dir / "config.toml"
    config_toml.write_text(
        """# Saisonxform Demo Configuration
# Generated by: sf demo

[paths]
input_dir = "Input"
reference_dir = "Reference"
output_dir = "Output"
archive_dir = "Archive"

[processing]
min_attendees = 2
max_attendees = 8

[processing.primary_id_weights]
"2" = 0.9  # 90% probability for ID 2
"1" = 0.1  # 10% probability for ID 1
""",
        encoding="utf-8",
    )

    # Success message
    typer.echo("\n✅ Demo files created successfully!\n")
    typer.echo(f"📁 Demo directory: {output_dir}\n")
    typer.echo("Directory structure:")
    typer.echo(f"  {output_dir}/")
    typer.echo("  ├── Input/")
    typer.echo("  │   └── 202510_sample.csv  (5 transactions)")
    typer.echo("  ├── Reference/")
    typer.echo("  │   └── NameList.csv        (8 attendees)")
    typer.echo("  ├── Output/                 (empty, for results)")
    typer.echo("  └── config.toml             (configuration file)\n")

    typer.echo("Next steps:")
    typer.echo("  1. Change to demo directory:")
    typer.echo(f"     cd {output_dir}\n")
    typer.echo("  2. Process the demo files (config.toml will be auto-detected):")
    typer.echo("     sf --verbose")
    typer.echo("     # or with explicit paths:")
    typer.echo("     sf --input Input --reference Reference --output Output --verbose\n")
    typer.echo("  3. View the results:")
    typer.echo("     open Output/202510_sample.html\n")
    typer.echo("💡 Tip: The config.toml file sets up all paths automatically!")
    typer.echo("   Just cd into the demo directory and run 'sf' to process.\n")


def main() -> int:
    """Main entry point for the CLI.

    This function is called by the console script entry point.
    Returns exit code for compatibility with existing tests.
    """
    try:
        app()
        return 0
    except (typer.Exit, SystemExit) as e:
        # SystemExit includes both success (0) and error codes
        if isinstance(e, SystemExit):
            return e.code if isinstance(e.code, int) else 1
        return e.exit_code
    except Exception:
        return 1


# Module invocation support: python -m saisonxform.cli
if __name__ == "__main__":
    sys.exit(main())
