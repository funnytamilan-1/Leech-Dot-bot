"""Secure admin entry point for the Leech Dot Bot web control center."""
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..core.config_manager import Config
from ..helper.ext_utils.bot_utils import new_task
from ..helper.telegram_helper.message_utils import send_message
from web.panel_auth import create_ticket


@new_task
async def webpanel(_, message):
    user = getattr(message, "from_user", None)
    if not user or not message.chat or message.chat.type != ChatType.PRIVATE:
        return await send_message(message, "For security, open a private chat with the bot and send /webpanel there.")

    secret = str(Config.WEBPANEL_SECRET or "")
    base_url = str(Config.WEBPANEL_BASE_URL or "").strip().rstrip("/")
    if not base_url.startswith("https://"):
        return await send_message(message, "<b>Web panel is not configured.</b> Set <code>WEBPANEL_BASE_URL</code> to your HTTPS VPS URL and configure <code>WEBPANEL_SECRET</code> with a random secret of at least 32 characters.")
    try:
        ticket = create_ticket(user.id, secret, Config.WEBPANEL_TICKET_TTL)
    except (ValueError, TypeError):
        return await send_message(message, "<b>Web panel security is not configured.</b> Set <code>WEBPANEL_SECRET</code> to a random secret of at least 32 characters.")

    # URL fragments are not sent in HTTP requests or normal access logs.
    url = f"{base_url}/webpanel#ticket={ticket}"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔐 Open Admin Control Center", url=url)]])
    await send_message(message, "<b>🔐 Leech Dot Bot — Admin Control Center</b>\n\nThis short-lived admin link expires automatically. Keep it private and do not forward it.", reply_markup=keyboard)
