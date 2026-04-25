# M4 Core

Discord bot for the Immie server, built with discord.py and cogs.

## Features

- Economy system (cores currency, gambling, transfers)
- Moderation (ban, kick, timeout, warn, purge)
- Fun commands (8ball, ship, roast, impostor, etc.)
- Utility (weather, translate, reminders, QR, polls)
- AI chat via Slug (Groq API)
- Anonymous confessions, Hall of Fame, welcome messages
- Remote eval console, hot-reload, GitHub pull

## Dependencies

```
discord.py>=2.3.0
aiohttp
groq
pyyaml
qrcode[pil]
Pillow
deep-translator
requests
```

Install with:

```bash
pip install -r requirements
```

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/notimm1e/M4-Core.git
cd M4-Core
```

**2. Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Set environment variables**

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `DISCORD_TOKEN` | ✓ | your bot token |
| `GROQ_KEY` | ✓ | groq api key for slug ai chat |
| `OPENWEATHER_KEY` | ✓ | openweathermap key for `!weather` |

**4. Configure `config.yaml`**

Edit `config.yaml` at the root with your server's channel and guild IDs:

```yaml
guild_id: YOUR_GUILD_ID

channels:
  log: 0
  console: 0
  ai_chat: 0
  dictionary: 0
  confession: 0
  hall_of_fame: 0
  welcome: 0
```

You can also set channels at runtime using the set commands (e.g. `!setwelcome #channel`).

**5. Add yourself as admin**

Edit `admins.yaml`:

```yaml
- YOUR_DISCORD_USER_ID
```

**6. Run the bot**

```bash
python main.py
```

## Branches

- **main** — stable, production-ready
- **canary** — active development and testing

## Hot Reload

Use `!reload` to reload all cogs without restarting, or `!pull [branch]` to sync from GitHub and auto-reload.