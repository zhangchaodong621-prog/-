from __future__ import annotations

import json
from typing import Any

import requests


def _safe_float(v: Any) -> float | None:
    try:
        if v is None:
            return None
        return float(v)
    except Exception:  # noqa: BLE001
        return None


def fetch_top_gainers(limit: int = 10, timeout_s: int = 20) -> list[dict]:
    """
    Fetch A-share top gainers using Eastmoney push2 quote API.

    Notes:
    - `fs` tries to include Shanghai+Shenzhen A shares. If you want to include STAR/ChiNext, adjust `fs`.
    - `fid=f3` sorts by % change descending.
    """
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": 1,
        "pz": max(1, min(limit, 50)),
        "po": 1,  # desc
        "np": 1,
        "fltt": 2,
        "invt": 2,
        "fid": "f3",  # pct change
        "fs": "m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23",  # SH A, SZ A, STAR, ChiNext (common)
        "fields": "f12,f14,f3,f62,f100,f102,f103",
    }
    r = requests.get(url, params=params, timeout=timeout_s)
    r.raise_for_status()

    data = r.json()
    diff = (((data or {}).get("data") or {}).get("diff")) or []

    out: list[dict] = []
    for row in diff[:limit]:
        code = str(row.get("f12", "")).strip()
        name = str(row.get("f14", "")).strip()
        pct = _safe_float(row.get("f3"))
        # f100/f102/f103 are not stable across endpoints; treat as "tags" best-effort.
        tags = " | ".join(
            [str(x).strip() for x in [row.get("f100"), row.get("f102"), row.get("f103")] if x not in (None, "", 0)]
        )
        out.append({"code": code, "name": name, "pct": pct, "tags": tags})
    return out

