"""Helpers for reading config/config.yml."""
from pathlib import Path

import yaml

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "config.yml"


def load_config(path=None) -> dict:
    """Load the YAML config. Defaults to <project>/config/config.yml."""
    with open(path or DEFAULT_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def table_name(cfg: dict, key: str) -> str:
    """Return the fully qualified table name, e.g. steam_data.default.silver_games."""
    return f"{cfg['catalog']}.{cfg['schema']}.{cfg['tables'][key]}"


def raw_path(cfg: dict, key: str) -> str:
    """Return the full path of a raw file. key is 'games_file' or 'reviews_file'."""
    return f"{cfg['raw_data']['volume_path']}/{cfg['raw_data'][key]}"
