from __future__ import annotations

from pathlib import Path

import yaml


def load_pools_config() -> dict:
    root = Path(__file__).resolve().parents[2]
    cfg_path = root / "config" / "pools.yaml"
    with cfg_path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    if "pools" not in cfg:
        raise ValueError("config/pools.yaml missing `pools`.")
    if "overrides" not in cfg:
        cfg["overrides"] = {}
    if "behavior" not in cfg:
        cfg["behavior"] = {"notify_on_non_trading_day": False}
    return cfg

