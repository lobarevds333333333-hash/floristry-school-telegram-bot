import logging
from aiogram import Bot
from config import ADMIN_CHAT_ID

logger = logging.getLogger(__name__)

async def notify_admin(bot: Bot, lead_data: dict, crm_success: bool, crm_msg: str):
    """
    Sends a formatted notification message to the Telegram admin/manager.
    """
    if not ADMIN_CHAT_ID or ADMIN_CHAT_ID == 0:
        logger.warning("[Notification] ADMIN_CHAT_ID is not configured in .env. Skipping admin notification.")
        return

    lead_code = lead_data.get("lead_code", "Н/Д")
    name = lead_data.get("full_name", "Н/Д")
    phone = lead_data.get("phone", "Н/Д")
    email = lead_data.get("email", "Н/Д")
    course = lead_data.get("course", "Н/Д")
    username = lead_data.get("username")
    user_id = lead_data.get("user_id")

    tg_user_str = f"@{username}" if username else f"ID: {user_id}"
    crm_icon = "✅" if crm_success else "⚠️"

    message_text = (
        f"🚨 <b>НОВАЯ ЗАЯВКА #{lead_code}</b>\n\n"
        f"👤 <b>Имя:</b> {name}\n"
        f"📞 <b>Телефон:</b> {phone}\n"
        f"✉️ <b>Email:</b> {email}\n"
        f"🎓 <b>Направление:</b> {course}\n"
        f"💬 <b>Telegram:</b> {tg_user_str}\n\n"
        f"📊 <b>Статус CRM:</b> {crm_icon} {crm_msg}"
    )

    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=message_text,
            parse_mode="HTML"
        )
        logger.info(f"[Notification] Successfully notified admin #{ADMIN_CHAT_ID} for lead #{lead_code}")
    except Exception as e:
        logger.error(f"[Notification Error] Failed to send notification to admin #{ADMIN_CHAT_ID}: {e}")
