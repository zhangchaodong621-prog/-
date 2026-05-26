from __future__ import annotations

from datetime import date


def is_cn_trading_day(d: date) -> bool:
    # Minimal heuristic: Mon-Fri. If you need exact holidays, add a holiday calendar source.
    # 0=Mon ... 6=Sun
    return d.weekday() < 5

