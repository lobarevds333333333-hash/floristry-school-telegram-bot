import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.reply import get_main_menu_keyboard, get_cancel_keyboard
from utils.validators import validate_phone, validate_email
from services.db import save_lead
from services.crm import send_lead_to_crm
from services.notification import notify_admin
from config import COURSES_DATA

logger = logging.getLogger(__name__)

router = Router()

class ApplicationForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_course = State()


@router.message(F.text == "❌ Отмена")
async def cancel_form(message: Message, state: FSMContext):
    """
    Cancels form submission and clears state.
    """
    await state.clear()
    await message.answer(
        "❌ Заполнение заявки отменено.",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == "Пробный урок")
async def start_trial_lesson(message: Message, state: FSMContext):
    """
    Starts FSM form for a trial lesson from reply menu.
    """
    await state.clear()
    await state.update_data(course="Бесплатный пробный урок")
    await state.set_state(ApplicationForm.waiting_for_name)
    await message.answer(
        "✍️ <b>Запись на бесплатный пробный урок</b>\n\n"
        "Пожалуйста, введите Ваше <b>Имя и Фамилию</b>:",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )


@router.callback_query(F.data == "start_trial")
async def callback_start_trial(callback: CallbackQuery, state: FSMContext):
    """
    Starts FSM form for a trial lesson from inline button.
    """
    await state.clear()
    await state.update_data(course="Бесплатный пробный урок")
    await state.set_state(ApplicationForm.waiting_for_name)
    await callback.message.answer(
        "✍️ <b>Запись на бесплатный пробный урок</b>\n\n"
        "Пожалуйста, введите Ваше <b>Имя и Фамилию</b>:",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("enroll_"))
async def callback_enroll_course(callback: CallbackQuery, state: FSMContext):
    """
    Starts FSM form for a specific selected course.
    """
    course_key = callback.data.replace("enroll_", "")
    course_info = COURSES_DATA.get(course_key)
    course_title = course_info["title"] if course_info else "Выбранный курс"

    await state.clear()
    await state.update_data(course=course_title)
    await state.set_state(ApplicationForm.waiting_for_name)
    
    await callback.message.answer(
        f"✍️ <b>Запись на курс: {course_title}</b>\n\n"
        "Пожалуйста, введите Ваше <b>Имя и Фамилию</b>:",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )
    await callback.answer()


@router.message(ApplicationForm.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """
    Processes user name input and prompts for phone number.
    """
    name = message.text.strip()
    if len(name) < 2 or len(name) > 60:
        await message.answer(
            "⚠️ Пожалуйста, введите корректное имя (от 2 до 60 символов):"
        )
        return

    await state.update_data(full_name=name)
    await state.set_state(ApplicationForm.waiting_for_phone)
    await message.answer(
        f"Принято, <b>{name}</b>!\n\n"
        "📱 Введите ваш <b>номер телефона</b> для связи (например: <code>+79991234567</code> или <code>89991234567</code>):",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )


@router.message(ApplicationForm.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """
    Processes phone input with regex validation.
    """
    phone_raw = message.text.strip()
    is_valid, formatted_phone = validate_phone(phone_raw)

    if not is_valid:
        await message.answer(
            "❌ <b>Некорректный формат телефона!</b>\n\n"
            "Пожалуйста, введите телефон в правильном формате, например:\n"
            "• <code>+7 999 123-45-67</code>\n"
            "• <code>89991234567</code>",
            parse_mode="HTML",
            reply_markup=get_cancel_keyboard()
        )
        return

    await state.update_data(phone=formatted_phone)
    await state.set_state(ApplicationForm.waiting_for_email)
    await message.answer(
        f"Телефон сохранен: <b>{formatted_phone}</b>\n\n"
        "✉️ Введите ваш <b>E-mail</b> (например: <code>name@example.com</code>):",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )


@router.message(ApplicationForm.waiting_for_email)
async def process_email(message: Message, state: FSMContext, bot: Bot):
    """
    Processes email input with regex validation, saves lead, posts to CRM, notifies admin, and confirms to user.
    """
    email_raw = message.text.strip()
    if not validate_email(email_raw):
        await message.answer(
            "❌ <b>Некорректный E-mail!</b>\n\n"
            "Пожалуйста, проверьте правильность ввода (например: <code>user@domain.com</code>):",
            parse_mode="HTML",
            reply_markup=get_cancel_keyboard()
        )
        return

    # Gather data from FSM context
    user_data = await state.get_data()
    full_name = user_data["full_name"]
    phone = user_data["phone"]
    email = email_raw
    course = user_data.get("course", "Флористика")

    user_id = message.from_user.id
    username = message.from_user.username

    # 1. Save to local SQLite database and generate lead_code (#FL-XXXX)
    lead_info = await save_lead(
        user_id=user_id,
        username=username,
        full_name=full_name,
        phone=phone,
        email=email,
        course=course
    )

    lead_code = lead_info["lead_code"]

    # 2. Send POST request to CRM System
    crm_success, crm_msg = await send_lead_to_crm(lead_info)

    # 3. Send Telegram notification to Manager/Admin
    await notify_admin(bot, lead_info, crm_success, crm_msg)

    # Clear state and restore main keyboard
    await state.clear()

    # 4. Confirmation message to user with unique application ID
    user_confirmation_text = (
        f"🎉 <b>Ваша заявка успешно создана!</b>\n\n"
        f"🏷 <b>Уникальный номер заявки:</b> <code>#{lead_code}</code>\n"
        f"👤 <b>Имя:</b> {full_name}\n"
        f"📱 <b>Телефон:</b> {phone}\n"
        f"✉️ <b>Email:</b> {email}\n"
        f"🎓 <b>Направление:</b> {course}\n\n"
        f"Наш менеджер свяжется с Вами в ближайшее время для подтверждения записи и уточнения деталей. Спасибо, что выбрали «Цветочные Истории»! 💐"
    )

    await message.answer(
        text=user_confirmation_text,
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )
