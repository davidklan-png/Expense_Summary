"""Command-line interface for Saison Transform.

Provides the main entry point and CLI commands for the application.
"""

import sys
from pathlib import Path

from .config import Config


def validate_config() -> int:
    """Validate configuration and check directory setup.

    Returns:
        Exit code (0 = success, 1 = failure)
    """
    from saisonxform.config import Config

    print("Validating configuration...")
    print()

    try:
        # Load config
        config = Config()

        # Display configuration
        print(f"Input directory:     {config.input_dir}")
        print(f"Reference directory: {config.reference_dir}")
        print(f"Output directory:    {config.output_dir}")
        print(f"Archive directory:   {config.archive_dir}")
        print()

        # Validate directories
        print("Checking directories...")
        config.validate_directories()
        print("✓ All required directories exist")
        print()

        # Validate templates
        print("Checking templates...")
        config.validate_templates()
        print("✓ All required templates exist")
        print()

        print("=" * 60)
        print("Configuration validation complete - SUCCESS")
        print("=" * 60)

        return 0

    except FileNotFoundError as e:
        print(f"✗ ERROR: {e}")
        print()
        print("=" * 60)
        print("Configuration validation FAILED")
        print("=" * 60)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return 1


def process_files() -> int:
    """
    Process transaction CSV files from Input directory.

    Returns:
        Exit code (0 = success, 1 = failure)
    """
    import pandas as pd
    from saisonxform.config import Config
    from saisonxform.io import read_csv_with_detection, write_csv_utf8_bom
    from saisonxform.selectors import filter_relevant_transactions, estimate_attendee_count, sample_attendee_ids
    from saisonxform.reporting import generate_html_report

    # Load configuration
    config = Config()

    input_dir = config.input_dir
    reference_dir = config.reference_dir
    output_dir = config.output_dir

    # Load attendee reference
    namelist_path = reference_dir / 'NameList.csv'
    if not namelist_path.exists():
        print(f"ERROR: NameList.csv not found at {namelist_path}")
        return 1

    attendee_ref = pd.read_csv(namelist_path, encoding='utf-8')
    available_ids = attendee_ref['ID'].astype(str).tolist()

    # Find CSV files in input directory
    csv_files = list(input_dir.glob('*.csv'))
    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return 0

    print(f"Found {len(csv_files)} CSV file(s) to process")
    print()

    processed_count = 0
    error_count = 0

    for csv_file in csv_files:
        try:
            print(f"Processing: {csv_file.name}")

            # Read CSV
            df, encoding = read_csv_with_detection(csv_file)
            print(f"  - Detected encoding: {encoding}")

            if df.empty:
                print(f"  - SKIPPED: Empty file")
                continue

            # Filter relevant transactions
            relevant_df = filter_relevant_transactions(df)
            print(f"  - Found {len(relevant_df)} relevant transactions")

            if len(relevant_df) == 0:
                print(f"  - SKIPPED: No meeting/entertainment expenses found")
                continue

            # Process each relevant transaction
            attendee_counts = []
            id_assignments = []

            for _, row in relevant_df.iterrows():
                # Estimate attendee count
                amount = row.get('利用金額', 0)
                count = estimate_attendee_count(amount)
                attendee_counts.append(count)

                # Sample attendee IDs
                ids_dict = sample_attendee_ids(
                    count=count,
                    available_ids=available_ids,
                    return_dict=True
                )
                id_assignments.append(ids_dict)

            # Add attendee columns to relevant transactions
            relevant_df['出席者'] = attendee_counts

            for i in range(1, 9):
                col_name = f'ID{i}'
                relevant_df[col_name] = [assignment[col_name] for assignment in id_assignments]

            # Generate output files
            output_stem = csv_file.stem
            csv_output = output_dir / f"{output_stem}.csv"
            html_output = output_dir / f"{output_stem}.html"

            # Write processed CSV
            write_csv_utf8_bom(relevant_df, csv_output, handle_duplicates=True)
            print(f"  - CSV output: {csv_output.name}")

            # Generate HTML report
            html_path = generate_html_report(
                transactions=relevant_df,
                attendee_reference=attendee_ref,
                output_path=html_output,
                source_filename=csv_file.name,
                handle_duplicates=True
            )
            print(f"  - HTML report: {html_path.name}")

            processed_count += 1
            print(f"  ✓ SUCCESS")

        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            error_count += 1

        print()

    # Summary
    print("=" * 60)
    print(f"Processing complete:")
    print(f"  - Processed: {processed_count}")
    print(f"  - Errors: {error_count}")
    print(f"  - Total: {len(csv_files)}")
    print("=" * 60)

    return 0 if error_count == 0 else 1


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code
    """
    # Parse command
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "validate-config":
            return validate_config()
        elif command == "process":
            return process_files()
        else:
            print(f"Unknown command: {command}")
            print()

    # Default action: show usage
    print("Saison Transform - Financial Transaction Processor")
    print()
    print("Usage:")
    print("  saisonxform validate-config    Validate configuration and environment")
    print("  saisonxform process            Process CSV files from Input directory")
    print()
    print("Examples:")
    print("  saisonxform validate-config")
    print("  saisonxform process")
    return 0


if __name__ == "__main__":
    sys.exit(main())
