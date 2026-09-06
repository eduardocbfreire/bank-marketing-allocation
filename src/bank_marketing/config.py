"""Single entry point for every business assumption of the project.

Nothing in the notebooks or in src/ should hard-code a value that lives in
config/params.yaml. If the contact capacity or the value of a conversion
changes, only the YAML file changes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "params.yaml"


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Read config/params.yaml and return it as a plain dictionary."""
    config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def resolve(relative_path: str | Path) -> Path:
    """Turn a project-relative path from the config into an absolute path."""
    return PROJECT_ROOT / relative_path
