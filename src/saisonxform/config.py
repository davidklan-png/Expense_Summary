"""Configuration management for Saison Transform.

Handles loading configuration from multiple sources with precedence:
1. Environment variables (INPUT_DIR, REFERENCE_DIR, OUTPUT_DIR, ARCHIVE_DIR)
2. config.toml in project root
3. pyproject.toml [tool.saisonxform] section

All paths are resolved relative to the project root for relative paths.
"""

import os
import tomllib
from pathlib import Path
from typing import Any, Optional


class Config:
    """Configuration manager with precedence-based loading."""

    def __init__(self, project_root: Optional[Path] = None, config_file: Optional[Path] = None):
        """Initialize configuration.

        Args:
            project_root: Project root directory (defaults to parent of this file's grandparent)
            config_file: Optional path to config.toml file (overrides default location)
        """
        if project_root is None:
            # Determine project root: src/saisonxform/config.py -> go up 2 levels
            project_root = Path(__file__).parent.parent.parent

        self.project_root = project_root
        self.config_file = config_file
        self._config: dict[str, Any] = {}
        self._dir_overrides: dict[str, Path] = {}  # CLI overrides for directories
        self._load_config()

        # Processing configuration (Phase 5)
        self.min_attendees = self._config.get("min_attendees", 2)
        self.max_attendees = self._config.get("max_attendees", 8)
        self.primary_id_weights = self._config.get("primary_id_weights", {"2": 0.9, "1": 0.1})

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
        if self.config_file:
            # Use explicitly provided config file
            config_toml_path = self.config_file
        else:
            # Use default location
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
            templates_dir: Templates directory (defaults to project_root/templates)

        Raises:
            FileNotFoundError: If templates directory or required templates don't exist
        """
        if templates_dir is None:
            templates_dir = self.project_root / "templates"

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
