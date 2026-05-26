# A股涨幅榜 Top10 三池统计推送（Telegram / Gmail）

每天 **15:30（北京时间）** 抓取 **A股涨幅榜 Top10**，按你的三类资产池（科技成长池 / 红利防御池 / 题材博弈池）做数量统计，并推送到 **Telegram** 或 **Gmail**。

> 说明：要在“电脑没开机”时也能收到消息，需要把任务跑在云端。本项目默认提供 **GitHub Actions 定时运行**（免费额度内一般够用）。

## 1) 快速开始（推荐：Telegram）

1. 在 Telegram 里用 `@BotFather` 创建 bot，拿到 `TELEGRAM_BOT_TOKEN`
2. 获取你的 `TELEGRAM_CHAT_ID`（可以把 bot 拉到群里，用群的 chat_id）
3. 在 GitHub 仓库 `Settings -> Secrets and variables -> Actions -> Secrets` 添加：
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

然后把本项目推到你的 GitHub 仓库，Actions 会在每天北京时间 15:30 自动运行并推送。

## 2) Gmail 推送（可选）

如果你更想用邮件，添加以下 Secrets（二选一：SMTP 或 Gmail API；此仓库默认用 SMTP 更简单）：

- `SMTP_HOST`（例如 `smtp.gmail.com`）
- `SMTP_PORT`（例如 `587`）
- `SMTP_USER`（你的 Gmail 地址）
- `SMTP_PASS`（建议用 Gmail “应用专用密码”，不要用主密码）
- `MAIL_TO`（收件人，通常就是你自己）

## 3) 自定义三池规则

规则文件：`config/pools.yaml`

- `keywords`：匹配股票的“行业/概念/标签”（取决于数据源能返回什么字段）
- `overrides`：你可以把某些股票代码强制指定到某个池（优先级最高）

## 4) 本地运行（调试用）

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src\main.py
```

## 5) 注意

- 数据源使用公开行情接口（见 `src/providers/eastmoney.py`），若接口字段变更，可能需要更新解析逻辑。
- 15:30 是交易日收盘后不久；如遇节假日/周末，脚本会自动跳过推送（可在配置里改为仍推送“今日非交易日”提示）。

