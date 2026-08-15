from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Returns the main persistent Reply Keyboard matching user requirements.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="О школе"),
                KeyboardButton(text="Каталог курсов")
            ],
            [
                KeyboardButton(text="Акции"),
                KeyboardButton(text="Пробный урок")
            ],
            [
                KeyboardButton(text="Контакты")
            ]
        ],
        resize_keyboard=True,
        persistent=True
    )
    return keyboard


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """
    Keyboard for canceling FSM form entry.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True
    )
