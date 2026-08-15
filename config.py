import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))
CRM_WEBHOOK_URL = os.getenv("CRM_WEBHOOK_URL", "http://127.0.0.1:8000/api/lead")
DB_PATH = os.getenv("DB_PATH", "bot_database.db")

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
CATALOG_PDF_PATH = ASSETS_DIR / "catalog.pdf"
FOUNDER_PHOTO_PATH = ASSETS_DIR / "founder.jpg"

# Courses data dictionary
COURSES_DATA = {
    "beginner": {
        "title": "🌸 Флористика для начинающих",
        "price": "15 000 ₽",
        "duration": "4 недели (16 уроков)",
        "description": "Базовый курс по сборке букетов, уходу за срезанными цветами и основам колористики. Подходит для тех, кто хочет стартовать в профессии с нуля.",
    },
    "wedding": {
        "title": "💍 Свадебная флористика",
        "price": "28 000 ₽",
        "duration": "6 недель (24 урока)",
        "description": "Курс по созданию свадебных букетов, оформлению президиума, фотозон и выездных регистраций. Отработка сложных композиций.",
    },
    "commercial": {
        "title": "🌿 Коммерческий букет и декор",
        "price": "22 000 ₽",
        "duration": "5 недель (20 уроков)",
        "description": "Техники быстрых коммерческих сборок, упаковка премиум-класса, расчёт себестоимости и продажи букетов через соцсети.",
    }
}
