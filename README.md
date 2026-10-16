<div align="center">

<img src="assets/codedots-leechdot.svg" alt="Leech Dot Bot — CodeDots" width="100%"/>

# 𝗟ᴇᴇᴄʜ 𝗗ᴏᴛ 𝗕ᴏᴛ

### 𝗔ᴅᴠᴀɴᴄᴇᴅ 𝗧ᴇʟᴇɢʀᴀᴍ 𝗙ɪʟᴇ 𝗔ᴜᴛᴏᴍᴀᴛɪᴏɴ

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Platform-Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org/)
[![Made by](https://img.shields.io/badge/Made%20by-%40Code__Dots-7c5cff?style=for-the-badge)](https://t.me/Code_Dots)
[![Partner](https://img.shields.io/badge/Partner-%40CodeRips-22c7d6?style=for-the-badge)](https://t.me/CodeRips)

**𝗠ᴀᴅᴇ ʙʏ [@Code_Dots](https://t.me/Code_Dots) · 𝗣ᴀʀᴛɴᴇʀ: [@CodeRips](https://t.me/CodeRips)**

</div>

---

## 𝗔ʙᴏᴜᴛ 𝗧ʜɪs 𝗥ᴇᴘᴏsɪᴛᴏʀʏ

**Leech Dot Bot** is a Python-based Telegram automation project designed to manage file-transfer workflows from a Telegram bot. Its configuration includes options for leeching and mirroring, task limits, progress/status updates, batch-related controls, file naming and captions, media handling, cloud destinations, streaming, and optional media-processing integrations.

The repository includes bot configuration, dependency declarations, deployment-related files, and project assets. Available features depend on the configured services, credentials, enabled flags, and the current implementation.

## 𝗙ᴇᴀᴛᴜʀᴇ 𝗔ʀᴇᴀs

| 𝗠ᴏᴅᴜʟᴇ | 𝗪ʜᴀᴛ 𝗜ᴛ 𝗖ᴏᴠᴇʀs |
|---|---|
| 𝗧ᴀsᴋ 𝗖ᴏɴᴛʀᴏʟ | Configurable task limits, queues, status updates, and task notifications |
| 𝗟ᴇᴇᴄʜ & 𝗠ɪʀʀᴏʀ | Configuration switches for leech, mirror, bulk, multi-task, and torrent-related workflows |
| 𝗙ɪʟᴇ 𝗛ᴀɴᴅʟɪɴɢ | Upload size settings, file captions, prefixes/suffixes, duplicate checks, and excluded extensions |
| 𝗠ᴇᴅɪᴀ 𝗧ᴏᴏʟs | Optional FFmpeg commands, encoding, compression, watermark, and thumbnail settings |
| 𝗖ʟᴏᴜᴅ & 𝗦ᴛᴏʀᴀɢᴇ | Optional Google Drive, rclone, GoFile, PixelDrain, and other provider settings |
| 𝗟ɪɴᴋ & 𝗦ᴛʀᴇᴀᴍ | Configuration for streaming, cloud links, and service integrations |
| 𝗔ᴜᴛᴏᴍᴀᴛɪᴏɴ | Optional RSS, search, YouTube-DL, plugin, and external downloader settings |
| 𝗔ᴄᴄᴇss & 𝗦ᴇᴄᴜʀɪᴛʏ | Owner ID, authorized chats, sudo users, force-subscription IDs, and private credentials |
| 𝗣ᴇʀsᴏɴᴀʟɪᴢᴀᴛɪᴏɴ | Language, timezone, progress-bar, upload-description, and metadata options |

> **Note:** These are configuration-supported feature areas, not a guarantee that every integration is enabled or operational in every deployment. Verify a feature against its implementation and logs before relying on it.

## 𝗣ʀᴏᴊᴇᴄᴛ 𝗦ᴛʀᴜᴄᴛᴜʀᴇ

- `config.py` — configuration defaults and optional integration settings.
- `requirements.txt` — Python dependency list.
- `bot/` — bot application and supporting modules.
- `assets/` — repository visual assets.
- `.github/workflows/` — automated repository checks, where configured.
- `update.py` — startup/update-related behavior; review its environment flags before enabling optional update operations.

Some paths or modules may vary by branch. Use the repository tree as the source of truth for the current layout.

## 𝗥ᴇǫᴜɪʀᴇᴍᴇɴᴛs

- Python 3.10 or newer (use the version supported by the selected hosting environment).
- A Telegram bot token from [@BotFather](https://t.me/BotFather).
- Telegram API ID and API hash from [my.telegram.org](https://my.telegram.org/).
- Owner Telegram user ID.
- A supported deployment environment and any credentials needed for the integrations you enable.
- Optional database, storage, downloader, or media-processing services depending on your setup.

## 𝗤ᴜɪᴄᴋ 𝗦ᴇᴛᴜᴘ

### 𝟭. 𝗚ᴇᴛ 𝗧ʜᴇ 𝗖ᴏᴅᴇ

```bash
git clone https://github.com/funnytamilan-1/Leech-Dot-bot.git
cd Leech-Dot-bot
```

### 𝟮. 𝗖ʀᴇᴀᴛᴇ 𝗔 𝗩ɪʀᴛᴜᴀʟ 𝗘ɴᴠɪʀᴏɴᴍᴇɴᴛ

```bash
python -m venv .venv
```

Activate it:

- Linux/macOS: `source .venv/bin/activate`
- Windows PowerShell: `.venv\Scripts\Activate.ps1`

### 𝟯. 𝗜ɴsᴛᴀʟʟ 𝗗ᴇᴘᴇɴᴅᴇɴᴄɪᴇs

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 𝟰. 𝗦ᴇᴛ 𝗬ᴏᴜʀ 𝗘ɴᴠɪʀᴏɴᴍᴇɴᴛ

Configure the required settings using your hosting provider's private environment-variable dashboard or the configuration mechanism supported by the code.

| 𝗦ᴇᴛᴛɪɴɢ | 𝗣ᴜʀᴘᴏsᴇ |
|---|---|
| `BOT_TOKEN` | Telegram bot token |
| `OWNER_ID` | Telegram numeric user ID of the owner |
| `TELEGRAM_API` | Telegram API ID |
| `TELEGRAM_HASH` | Telegram API hash |
| `DATABASE_URL` | Optional database connection string, if used by the deployment |
| `UPSTREAM_REPO` | Optional update source; keep empty unless you intentionally configure one |

The exact names and required values are defined by the current source. Do not paste real credentials into README files, public issues, screenshots, or commits.

### 𝟱. 𝗦ᴛᴀʀᴛ 𝗧ʜᴇ 𝗕ᴏᴛ

Check the repository's actual entry-point and hosting start command before launching. Do not assume a generic command such as `python bot.py` is correct unless that file is the configured entry point.

## 𝗖ᴏɴғɪɢᴜʀᴀᴛɪᴏɴ 𝗚ᴜɪᴅᴇ

- Enable only the integrations you have configured and tested.
- Keep owner IDs and authorized-chat settings accurate.
- Set sensible task and concurrency limits for the hosting plan.
- Configure storage credentials and destinations separately for each provider.
- Review upload-size limits, Telegram API constraints, and available disk/RAM.
- Keep update and package-install behavior disabled unless you understand the operational impact.
- Use a persistent database/storage location when state must survive redeployments.
- Check the complete startup traceback rather than hiding errors behind generic messages.

## 𝗦ᴇᴄᴜʀɪᴛʏ 𝗕ᴇsᴛ 𝗣ʀᴀᴄᴛɪᴄᴇs

- **Never publish** `BOT_TOKEN`, API hashes, session strings, passwords, database URLs, or cloud-provider keys.
- Use hosting secrets/environment variables for sensitive values.
- Rotate any credential that has been exposed.
- Grant the bot only the permissions it needs.
- Only transfer or process files you own or are authorized to access.
- Review third-party integrations and their data-handling requirements before enabling them.

## 𝗧ʀᴏᴜʙʟᴇsʜᴏᴏᴛɪɴɢ

| 𝗣ʀᴏʙʟᴇᴍ | 𝗪ʜᴀᴛ 𝗧ᴏ 𝗖ʜᴇᴄᴋ |
|---|---|
| Bot fails at startup | Required environment variables, Python version, dependency installation, and the full traceback |
| Invalid token/API credentials | Re-check the token, API ID/hash, and secret formatting |
| Downloads/uploads are slow | Identify the slow stage, inspect network/disk/RAM usage, and check provider limits |
| Batch or queue does not finish | Review task limits, queue configuration, logs, and error handling |
| Storage integration fails | Verify provider credentials, destination IDs, permissions, and connectivity |
| State disappears after redeploy | Confirm the database and files use persistent storage |
| Optional update changes files | Review update flags and deployment configuration before enabling automatic updates |

## 𝗗ᴇᴠᴇʟᴏᴘᴍᴇɴᴛ & 𝗩ᴇʀɪғɪᴄᴀᴛɪᴏɴ

Before deploying a change, check:

- [ ] Python syntax and imports.
- [ ] Startup with valid configuration and startup failure with missing configuration.
- [ ] Single-file workflow and batch workflow.
- [ ] Progress reporting, cancellation, retries, and error messages.
- [ ] Large-file behavior within platform and hosting limits.
- [ ] Storage-provider integrations that you actually use.
- [ ] Restart and redeploy persistence.
- [ ] Deployment start command, health checks, and logs.

Do not mark a feature as fixed or tested until the corresponding check has actually passed.

## 𝗖ʀᴇᴅɪᴛs & 𝗦ᴜᴘᴘᴏʀᴛ

- **𝗠ᴀᴅᴇ ʙʏ:** [@Code_Dots](https://t.me/Code_Dots)
- **𝗣ᴀʀᴛɴᴇʀ:** [@CodeRips](https://t.me/CodeRips)
- **𝗥ᴇᴘᴏsɪᴛᴏʀʏ:** [Leech-Dot-bot on GitHub](https://github.com/funnytamilan-1/Leech-Dot-bot)

---

<div align="center">

### 𝗟ᴇᴇᴄʜ 𝗗ᴏᴛ · 𝗖ᴏᴅᴇ𝗗ᴏᴛs

**𝗕ᴜɪʟᴛ 𝗙ᴏʀ 𝗖ʟᴇᴀʀ 𝗪ᴏʀᴋғʟᴏᴡs, 𝗦ᴀғᴇ 𝗖ᴏɴғɪɢᴜʀᴀᴛɪᴏɴ, 𝗔ɴᴅ 𝗥ᴇʟɪᴀʙʟᴇ 𝗢ᴘᴇʀᴀᴛɪᴏɴ.**

</div>


## 𝗖ʀᴇᴅɪᴛs

**𝗠ᴀᴅᴇ ʙʏ [@Code_Dots](https://t.me/Code_Dots) · 𝗣ᴀʀᴛɴᴇʀ [@CodeRips](https://t.me/CodeRips)**

See [NOTICE.md](NOTICE.md) for project credit and license notes. The upstream AGPL-3.0 license text remains unchanged.


## Secure VPS Web Control Center

The owner and configured sudo users can send `/webpanel` to receive a short-lived signed admin link. Configure these private environment variables on the same VPS deployment:

- `WEBPANEL_BASE_URL`: public HTTPS origin for the web server, e.g. `https://bot.example.com`.
- `WEBPANEL_SECRET`: random secret with at least 32 characters. Do not commit it.
- `WEBPANEL_TICKET_TTL`: signed-link lifetime in seconds (60–1800; default 900).
- `LEECH_DOT_RUNTIME_SETTINGS`: optional absolute path for the shared runtime settings file. Bot and web workers must use the same file path; default is `runtime_settings.json` in their working directory.

The control center supports runtime transfer settings. The private runtime settings file is ignored by Git and is written atomically. Serve the panel only over HTTPS. Never share the admin link or publish the signing secret.

The panel uses the configured `OWNER_ID` and `SUDO_USERS` values for server-side authorization; hiding the dashboard in the browser is not an access-control mechanism.
