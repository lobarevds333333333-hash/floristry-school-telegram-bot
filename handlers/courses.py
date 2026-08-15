import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile

from config import CATALOG_PDF_PATH, COURSES_DATA
from keyboards.inline import (
    get_courses_inline_keyboard,
    get_course_detail_keyboard
)

router = Router()

async def safe_edit_or_answer(callback: CallbackQuery, text: str, reply_markup=None):
    """
    Safely edits text, caption, or sends a new message depending on whether the original message was a document or text message.
    """
    if callback.message.document or callback.message.photo:
        try:
            await callback.message.edit_caption(
                caption=text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
            return
        except Exception:
            pass

    try:
        await callback.message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    except Exception:
        await callback.message.answer(
            text=text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )


@router.message(F.text == "Каталог курсов")
async def show_catalog(message: Message):
    """
    Sends catalog PDF file and course catalog overview with inline selection buttons.
    """
    caption = (
        "📚 <b>Каталог курсов школы «Цветочные Истории»</b>\n\n"
        "Мы подготовили для вас полный справочник по всем программам обучения. "
        "Скачайте PDF-файл выше или выберите интересующий курс в меню ниже для просмотра деталей:"
    )

    # Check if catalog.pdf exists and send document
    if os.path.exists(CATALOG_PDF_PATH):
        pdf_file = FSInputFile(CATALOG_PDF_PATH, filename="Каталог_Курсов_Цветочные_Истории.pdf")
        await message.answer_document(
            document=pdf_file,
            caption=caption,
            parse_mode="HTML",
            reply_markup=get_courses_inline_keyboard()
        )
    else:
        await message.answer(
            text=caption,
            parse_mode="HTML",
            reply_markup=get_courses_inline_keyboard()
        )


@router.callback_query(F.data == "back_to_courses")
async def callback_back_to_courses(callback: CallbackQuery):
    """
    Returns to course catalog overview.
    """
    caption = (
        "📚 <b>Каталог курсов школы «Цветочные Истории»</b>\n\n"
        "Выберите интересующий курс из списка ниже:"
    )
    await safe_edit_or_answer(
        callback=callback,
        text=caption,
        reply_markup=get_courses_inline_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("course_"))
async def callback_course_detail(callback: CallbackQuery):
    """
    Shows detailed information for selected course.
    """
    course_key = callback.data.replace("course_", "")
    course_info = COURSES_DATA.get(course_key)

    if not course_info:
        await callback.answer("Курс не найден", show_alert=True)
        return

    detail_text = (
        f"<b>{course_info['title']}</b>\n\n"
        f"⏱ <b>Длительность:</b> {course_info['duration']}\n"
        f"💰 <b>Стоимость:</b> {course_info['price']}\n\n"
        f"📝 <b>Описание:</b>\n{course_info['description']}\n\n"
        f"Нажмите кнопку ниже, чтобы записаться на этот курс!"
    )

    await safe_edit_or_answer(
        callback=callback,
        text=detail_text,
        reply_markup=get_course_detail_keyboard(course_key)
    )
    await callback.answer()
