import logging
import aiohttp
from typing import Dict, Any, Tuple
from config import CRM_WEBHOOK_URL
from services.db import update_crm_status

logger = logging.getLogger(__name__)

async def send_lead_to_crm(lead_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Sends lead data to CRM system via POST request.
    Supports generic webhook format and Bitrix24 REST API.
    Returns (success: bool, response_message: str).
    """
    lead_code = lead_data["lead_code"]
    name = lead_data["full_name"]
    phone = lead_data["phone"]
    email = lead_data["email"]
    course = lead_data["course"]
    username = lead_data.get("username", "")

    # Detect if CRM_WEBHOOK_URL is Bitrix24 REST API
    is_bitrix = "crm.lead.add" in CRM_WEBHOOK_URL.lower() or "bitrix" in CRM_WEBHOOK_URL.lower()

    if is_bitrix:
        payload = {
            "fields": {
                "TITLE": f"Заявка #{lead_code} - Школа флористики",
                "NAME": name,
                "PHONE": [{"VALUE": phone, "VALUE_TYPE": "WORK"}],
                "EMAIL": [{"VALUE": email, "VALUE_TYPE": "WORK"}],
                "COMMENTS": f"Курс/Направление: {course}\nTelegram: @{username}\nНомер заявки: {lead_code}"
            }
        }
    else:
        payload = {
            "lead_code": lead_code,
            "name": name,
            "phone": phone,
            "email": email,
            "course": course,
            "username": username,
            "comment": f"Заявка на {course} (ID #{lead_code})"
        }

    logger.info(f"[CRM] Sending lead #{lead_code} to {CRM_WEBHOOK_URL}...")

    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(CRM_WEBHOOK_URL, json=payload) as response:
                status = response.status
                text = await response.text()

                if status in (200, 201):
                    logger.info(f"[CRM Success] Lead #{lead_code} sent successfully. Response: {text[:100]}")
                    await update_crm_status(lead_code, "sent_to_crm")
                    return True, "Заявка успешно переведена в CRM"
                else:
                    logger.error(f"[CRM Error] Failed to send lead #{lead_code}. HTTP Status: {status}, Response: {text[:200]}")
                    await update_crm_status(lead_code, f"error_http_{status}")
                    return False, f"Ошибка CRM API (Статус: {status})"

    except aiohttp.ClientConnectorError as err:
        logger.error(f"[CRM Network Error] Cannot connect to CRM server {CRM_WEBHOOK_URL}: {err}")
        await update_crm_status(lead_code, "connection_error")
        return False, "Ошибка подключения к серверу CRM"

    except Exception as e:
        logger.error(f"[CRM Exception] Exception sending lead #{lead_code}: {e}")
        await update_crm_status(lead_code, "exception")
        return False, f"Ошибка при отправке: {str(e)}"
