from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_courses_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Returns inline keyboard for selecting specific courses in the catalog.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌸 Флористика для начинающих",
                    callback_data="course_beginner"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💍 Свадебная флористика",
                    callback_data="course_wedding"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌿 Коммерческий букет",
                    callback_data="course_commercial"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎁 Записаться на пробный урок",
                    callback_data="start_trial"
                )
            ]
        ]
    )
    return keyboard


def get_course_detail_keyboard(course_key: str) -> InlineKeyboardMarkup:
    """
    Returns inline keyboard for a specific course details view.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✍️ Записаться на данный курс",
                    callback_data=f"enroll_{course_key}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📜 Все курсы",
                    callback_data="back_to_courses"
                )
            ]
        ]
    )
    return keyboard


def get_promo_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Returns inline keyboard for promo section.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎁 Записаться на бесплатный урок",
                    callback_data="start_trial"
                )
            ]
        ]
    )
    return keyboard
