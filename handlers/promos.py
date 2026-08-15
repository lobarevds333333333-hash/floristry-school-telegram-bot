from aiogram import Router, F
from aiogram.types import Message

from keyboards.inline import get_promo_inline_keyboard

router = Router()

@router.message(F.text == "Акции")
async def show_promotions(message: Message):
    """
    Displays current special offers and promo deals with a trial lesson CTA button.
    """
    promo_text = (
        "🔥 <b>АКТУАЛЬНЫЕ АКЦИИ И СПЕЦПРЕДЛОЖЕНИЯ</b> 🔥\n\n"
        "1️⃣ <b>Бесплатный вводный видеоурок «Секреты свежести цветов»</b>\n"
        "Получите прямой доступ к видеоуроку и практикуйтесь бесплатно при записи сегодня!\n\n"
        "2️⃣ <b>Скидка 20% при раннем бронировании!</b>\n"
        "Запишитесь на флагманский курс «Флористика для начинающих» до конца недели и получите набор флористических инструментов в подарок ✂️💐\n\n"
        "👇 <i>Нажмите кнопку ниже, чтобы забронировать бесплатный пробный урок и скидку:</i>"
    )

    await message.answer(
        text=promo_text,
        parse_mode="HTML",
        reply_markup=get_promo_inline_keyboard()
    )
