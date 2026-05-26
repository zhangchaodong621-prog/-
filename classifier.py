from __future__ import annotations

import re


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", (s or "").lower())


def classify_stock(item: dict, cfg: dict) -> str:
    """
    Heuristic classifier:
    - overrides by code first
    - then keyword matching against concatenated tag text (name + tags)
    - returns pool key, or "unknown"
    """
    code = str(item.get("code", "")).strip()
    overrides = cfg.get("overrides", {}) or {}
    if code and code in overrides:
        return str(overrides[code]).strip()

    haystack = _norm(f"{item.get('name','')} {item.get('tags','')}")
    for pool_key, pool in (cfg.get("pools", {}) or {}).items():
        for kw in pool.get("keywords", []) or []:
            if _norm(str(kw)) and _norm(str(kw)) in haystack:
                return pool_key
    return "unknown"

