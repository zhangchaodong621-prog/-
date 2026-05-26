from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from utils.calendar_cn import is_cn_trading_day
from utils.config import load_pools_config
from utils.classifier import classify_stock
from providers.eastmoney import fetch_top_gainers
from senders.gmail_smtp import send_gmail_smtp
from senders.telegram import send_telegram


@dataclass(frozen=True)
class SendTargets:
    telegram_enabled: bool
    gmail_enabled: bool


CN_TZ = timezone(timedelta(hours=8))


def now_cn() -> datetime:
    return datetime.now(timezone.utc).astimezone(CN_TZ)


def detect_targets() -> SendTargets:
    telegram_enabled = bool(os.getenv("TELEGRAM_BOT_TOKEN")) and bool(os.getenv("TELEGRAM_CHAT_ID"))
    gmail_enabled = bool(os.getenv("SMTP_HOST")) and bool(os.getenv("SMTP_USER")) and bool(os.getenv("SMTP_PASS")) and bool(
        os.getenv("MAIL_TO")
    )
    return SendTargets(telegram_enabled=telegram_enabled, gmail_enabled=gmail_enabled)


def build_message(date_cn: datetime, top10: list[dict], pools_cfg: dict) -> str:
    pool_keys = list(pools_cfg["pools"].keys())
    counts = {k: 0 for k in pool_keys}
    unknown: list[dict] = []

    lines = []
    lines.append(f"A股涨幅榜 Top10（三池统计）")
    lines.append(f"日期：{date_cn.strftime('%Y-%m-%d')}（北京时间）")
    lines.append("")

    for item in top10:
        pool = classify_stock(item, pools_cfg)
        item["pool"] = pool
        if pool in counts:
            counts[pool] += 1
        else:
            unknown.append(item)

    # Summary
    lines.append("统计：")
    for k in pool_keys:
        lines.append(f"- {pools_cfg['pools'][k]['name']}：{counts[k]} 只")
    if unknown:
        lines.append(f"- 未归类：{len(unknown)} 只")
    lines.append("")

    # Detail
    lines.append("Top10 明细：")
    for idx, item in enumerate(top10, start=1):
        pool_name = pools_cfg["pools"].get(item["pool"], {}).get("name", "未归类")
        zdf = item.get("pct", None)
        zdf_s = f"{zdf:.2f}%" if isinstance(zdf, (int, float)) else "?"
        tags = item.get("tags", "")
        lines.append(f"{idx}. {item['name']}({item['code']}) {zdf_s} | {pool_name} | {tags}")

    return "\n".join(lines)


def main() -> int:
    pools_cfg = load_pools_config()
    now = now_cn()

    if not is_cn_trading_day(now.date()):
        if not pools_cfg.get("behavior", {}).get("notify_on_non_trading_day", False):
            print("Non-trading day; skip.")
            return 0

    top10 = fetch_top_gainers(limit=10)
    if not top10:
        raise RuntimeError("Failed to fetch top gainers (empty result).")

    msg = build_message(now, top10, pools_cfg)

    targets = detect_targets()
    if not (targets.telegram_enabled or targets.gmail_enabled):
        print(msg)
        print("\n(No sender configured. Set Telegram or SMTP env vars.)")
        return 0

    errors: list[str] = []
    if targets.telegram_enabled:
        try:
            send_telegram(msg)
        except Exception as e:  # noqa: BLE001
            errors.append(f"Telegram send failed: {e}")
    if targets.gmail_enabled:
        try:
            send_gmail_smtp(subject="A股涨幅榜Top10三池统计", body=msg)
        except Exception as e:  # noqa: BLE001
            errors.append(f"Gmail SMTP send failed: {e}")

    if errors:
        raise RuntimeError(" | ".join(errors))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
