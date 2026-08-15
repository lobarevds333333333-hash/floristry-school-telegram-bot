import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.reply import get_main_menu_keyboard
from config import FOUNDER_PHOTO_PATH

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """
    Handles /start command: resets FSM state and displays welcome text with main keyboard.
    """
    await state.clear()
    welcome_text = (
        "Добро пожаловать в онлайн-школу Цветочные Истории! 💐 "
        "Здесь вы можете узнать всё о курсах по флористике, получить первый урок "
        "бесплатно и задать вопрос менеджеру. Выберите нужный раздел в меню ниже."
    )
    await message.answer(
        text=welcome_text,
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == "О школе")
async def show_about_school(message: Message):
    """
    Displays school information and founder bio with photo.
    """
    about_text = (
        "🌸 <b>Школа флористики «Цветочные Истории»</b>\n\n"
        "Мы — международная онлайн-школа современной флористики и декора. "
        "За 6 лет работы мы обучили более 3500 учеников из 25 стран мира.\n\n"
        "👑 <b>Основатель школы — Анна Цветочная:</b>\n"
        "• Шеф-флорист с 12-летним практическим стажем.\n"
        "• Победитель международных флористических конкурсов.\n"
        "• Автор патентованных техник сборки растрепанных и свадебных букетов.\n\n"
        "💡 <i>Наша миссия — превратить ваше увлечение цветами в любимую и доходную профессию!</i>"
    )

    if os.path.exists(FOUNDER_PHOTO_PATH):
        photo = FSInputFile(FOUNDER_PHOTO_PATH)
        await message.answer_photo(
            photo=photo,
            caption=about_text,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            text=about_text,
            parse_mode="HTML"
        )


@router.message(F.text == "Контакты")
async def show_contacts(message: Message):
    """
    Displays school contact information.
    """
    contacts_text = (
        "📞 <b>Контакты школы «Цветочные Истории»</b>\n\n"
        "📍 <b>Адрес студии:</b> г. Москва, ул. Цветочная, д. 15, стр. 2\n"
        "📱 <b>Телефон / WhatsApp:</b> +7 (999) 000-11-22\n"
        "✉️ <b>Email:</b> info@flower-stories.ru\n"
        "🌐 <b>Сайт:</b> flower-stories-school.ru\n\n"
        "💬 <b>Мы в соцсетях:</b>\n"
        "• Telegram-канал: @flower_stories_official\n"
        "• VKontakte: vk.com/flower_stories_school\n\n"
        "⏰ <b>Режим работы отдела заботы:</b> Ежедневно с 09:00 до 21:00 (МСК)"
    )
    await message.answer(
        text=contacts_text,
        parse_mode="HTML"
    )
