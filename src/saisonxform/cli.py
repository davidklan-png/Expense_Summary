"""Command-line interface for Saison Transform.

Provides the main entry point and CLI commands for the application.
"""

import sys
from pathlib import Path

from .config import Config


def validate_config() -> int:
    """Validate configuration and environment setup.

    This is a no-op CLI skeleton for Phase 1 that loads configuration,
    verifies directory and template presence, and exits with status code 0
    without processing data.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        print("Saison Transform - Configuration Validation")
        print("=" * 50)
        print()

        # Load configuration
        print("Loading configuration...")
        config = Config()

        # Display configuration precedence
        print("Configuration precedence order:")
        print("  1. Environment variables (INPUT_DIR, REFERENCE_DIR, OUTPUT_DIR, ARCHIVE_DIR)")
        print("  2. config.toml")
        print("  3. pyproject.toml [tool.saisonxform]")
        print()

        # Display resolved paths
        print("Resolved directories:")
        print(f"  Input:     {config.input_dir}")
        print(f"  Reference: {config.reference_dir}")
        print(f"  Output:    {config.output_dir}")
        print(f"  Archive:   {config.archive_dir}")
        print()

        # Validate directories
        print("Validating required directories...")
        config.validate_directories()
        print("✓ All required directories exist")
        print()

        # Validate templates
        print("Validating template files...")
        config.validate_templates()
        print("✓ All required templates exist")
        print()

        print("=" * 50)
        print("Configuration validation successful!")
        return 0

    except FileNotFoundError as e:
        print(f"✗ Validation failed: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code
    """
    # For Phase 1, we only have validate-config command
    if len(sys.argv) > 1 and sys.argv[1] == "validate-config":
        return validate_config()

    # Default action: show usage
    print("Saison Transform - Financial Transaction Processor")
    print()
    print("Usage:")
    print("  saisonxform validate-config    Validate configuration and environment")
    print()
    print("Phase 1 includes only configuration validation.")
    print("Data processing commands will be added in Phase 2.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
