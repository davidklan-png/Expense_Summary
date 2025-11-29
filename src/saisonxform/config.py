"""Configuration management for Saison Transform.

Handles loading configuration from multiple sources with precedence:
1. Environment variables (INPUT_DIR, REFERENCE_DIR, OUTPUT_DIR, ARCHIVE_DIR)
2. Explicitly provided config file (--config option)
3. data/reference/config.toml (persistent configuration)
4. config.toml in project root (fallback)
5. pyproject.toml [tool.saisonxform] section (defaults)

All paths are resolved relative to the project root for relative paths.
"""

import os
import sys
from pathlib import Path
from typing import Any, Optional

# Python 3.10 compatibility: use tomli for older versions
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib  # type: ignore[import-not-found,unused-ignore]
    except ImportError:
        raise ImportError("tomli is required for Python < 3.11. Install with: pip install tomli")


class Config:
    """Configuration manager with precedence-based loading."""

    def __init__(self, project_root: Optional[Path] = None, config_file: Optional[Path] = None):
        """Initialize configuration.

        Args:
            project_root: Project root directory (defaults to current working directory)
            config_file: Optional path to config.toml file (overrides default location)
        """
        if project_root is None:
            if config_file is not None:
                # Use config file's parent directory as project root
                # Resolve the config file path first, then get its parent
                project_root = Path(config_file).resolve().parent
            else:
                # Use current working directory as project root
                project_root = Path.cwd()

        self.project_root = project_root
        self.config_file = config_file
        self._config: dict[str, Any] = {}
        self._dir_overrides: dict[str, Path] = {}  # CLI overrides for directories
        self._load_config()

        # Processing configuration (Phase 5)
        self.min_attendees = self._config.get("min_attendees", 2)
        self.max_attendees = self._config.get("max_attendees", 8)
        self.primary_id_weights = self._config.get("primary_id_weights", {"2": 0.9, "1": 0.1})

        # Amount-based attendee estimation (optional)
        self.amount_based_attendees = self._load_amount_based_config()

    def _load_config(self) -> None:
        """Load configuration from all sources with proper precedence."""
        # Start with pyproject.toml defaults
        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                pyproject_data = tomllib.load(f)
                if "tool" in pyproject_data and "saisonxform" in pyproject_data["tool"]:
                    self._config.update(pyproject_data["tool"]["saisonxform"])

        # Override with config.toml if present
        # Priority: 1. Explicitly provided, 2. data/reference/config.toml, 3. config.toml (root)
        if self.config_file:
            # Use explicitly provided config file
            config_toml_path = self.config_file
        else:
            # Check data/reference/config.toml first (persistent config)
            reference_config = self.project_root / "data" / "reference" / "config.toml"
            if reference_config.exists():
                config_toml_path = reference_config
            else:
                # Fall back to root config.toml
                config_toml_path = self.project_root / "config.toml"

        if config_toml_path.exists():
            with open(config_toml_path, "rb") as f:
                config_data = tomllib.load(f)
                # Flatten nested structure (paths, processing, output, archival)
                for section in config_data.values():
                    if isinstance(section, dict):
                        self._config.update(section)

        # Override with environment variables (highest priority)
        env_overrides = {
            "input_dir": os.getenv("INPUT_DIR"),
            "reference_dir": os.getenv("REFERENCE_DIR"),
            "output_dir": os.getenv("OUTPUT_DIR"),
            "archive_dir": os.getenv("ARCHIVE_DIR"),
        }
        for key, value in env_overrides.items():
            if value is not None:
                self._config[key] = value

    def _load_amount_based_config(self) -> dict[str, Any] | None:
        """Load and validate amount-based attendee estimation configuration.

        Returns:
            Dict with 'brackets' and 'cost_per_person' keys, or None if not configured/disabled

        Warns (non-fatal) if configuration is invalid.
        """
        import warnings

        amount_config = self._config.get("amount_based_attendees")
        if not amount_config or not isinstance(amount_config, dict):
            # Not configured - use default random behavior
            return None

        # Check if explicitly disabled
        if not amount_config.get("enabled", True):
            # User disabled amount-based logic - use random behavior
            return None

        try:
            # Parse brackets from config
            brackets_config = amount_config.get("brackets", {})
            cost_per_person = amount_config.get("cost_per_person", 3000)

            # Convert string keys "min-max" to tuple keys (min, max)
            parsed_brackets = {}
            for range_str, attendee_range in brackets_config.items():
                try:
                    min_amount, max_amount = map(int, range_str.split("-"))
                    if min_amount < 0 or max_amount < min_amount:
                        raise ValueError(f"Invalid range: {range_str}")

                    if not isinstance(attendee_range, dict):
                        raise ValueError(f"Bracket {range_str} must have min/max attendees")

                    min_att = attendee_range.get("min")
                    max_att = attendee_range.get("max")

                    if min_att is None or max_att is None:
                        raise ValueError(f"Bracket {range_str} missing min or max attendees")

                    if min_att < 1 or max_att < min_att:
                        raise ValueError(f"Invalid attendee range in {range_str}: min={min_att}, max={max_att}")

                    parsed_brackets[(min_amount, max_amount)] = {"min": min_att, "max": max_att}

                except Exception as e:
                    warnings.warn(f"Skipping invalid amount bracket '{range_str}': {e}")
                    continue

            if not parsed_brackets:
                warnings.warn("No valid amount brackets found. Using default random behavior.")
                return None

            return {
                "brackets": parsed_brackets,
                "cost_per_person": cost_per_person,
            }

        except Exception as e:
            warnings.warn(f"Failed to load amount-based config: {e}. Using default random behavior.")
            return None

    def _resolve_path(self, path_str: str) -> Path:
        """Resolve a path string relative to project root if not absolute.

        Args:
            path_str: Path string (relative or absolute)

        Returns:
            Resolved absolute Path object
        """
        path = Path(path_str)
        if path.is_absolute():
            return path
        return (self.project_root / path).resolve()

    @property
    def input_dir(self) -> Path:
        """Get resolved input directory path."""
        if "input_dir" in self._dir_overrides:
            return self._dir_overrides["input_dir"]
        return self._resolve_path(self._config.get("input_dir", "../Input"))

    @input_dir.setter
    def input_dir(self, value: Path) -> None:
        """Set input directory override."""
        self._dir_overrides["input_dir"] = value

    @property
    def reference_dir(self) -> Path:
        """Get resolved reference directory path."""
        if "reference_dir" in self._dir_overrides:
            return self._dir_overrides["reference_dir"]
        return self._resolve_path(self._config.get("reference_dir", "../Reference"))

    @reference_dir.setter
    def reference_dir(self, value: Path) -> None:
        """Set reference directory override."""
        self._dir_overrides["reference_dir"] = value

    @property
    def output_dir(self) -> Path:
        """Get resolved output directory path."""
        if "output_dir" in self._dir_overrides:
            return self._dir_overrides["output_dir"]
        return self._resolve_path(self._config.get("output_dir", "../Output"))

    @output_dir.setter
    def output_dir(self, value: Path) -> None:
        """Set output directory override."""
        self._dir_overrides["output_dir"] = value

    @property
    def archive_dir(self) -> Path:
        """Get resolved archive directory path."""
        if "archive_dir" in self._dir_overrides:
            return self._dir_overrides["archive_dir"]
        return self._resolve_path(self._config.get("archive_dir", "../Archive"))

    @archive_dir.setter
    def archive_dir(self, value: Path) -> None:
        """Set archive directory override."""
        self._dir_overrides["archive_dir"] = value

    def validate_directories(self) -> None:
        """Validate that required directories exist.

        Raises:
            FileNotFoundError: If required directories (Input, Reference, Output) don't exist
        """
        required_dirs = [
            ("Input", self.input_dir),
            ("Reference", self.reference_dir),
            ("Output", self.output_dir),
        ]

        missing = []
        for name, path in required_dirs:
            if not path.exists():
                missing.append(f"{name}: {path}")

        if missing:
            raise FileNotFoundError("Required directories not found:\n" + "\n".join(f"  - {m}" for m in missing))

        # Archive is optional - will be created on first use
        if not self.archive_dir.exists():
            print(f"Note: Archive directory will be created on first use: {self.archive_dir}")

    def validate_templates(self, templates_dir: Optional[Path] = None) -> None:
        """Validate that required template files exist.

        Args:
            templates_dir: Templates directory (defaults to package templates/)

        Raises:
            FileNotFoundError: If templates directory or required templates don't exist
        """
        if templates_dir is None:
            # Templates are now inside the package
            templates_dir = Path(__file__).parent / "templates"

        if not templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {templates_dir}")

        required_templates = ["report.html.j2"]
        missing = []
        for template in required_templates:
            template_path = templates_dir / template
            if not template_path.exists():
                missing.append(str(template_path))

        if missing:
            raise FileNotFoundError("Required template files not found:\n" + "\n".join(f"  - {m}" for m in missing))

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
