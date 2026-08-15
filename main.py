import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, ASSETS_DIR
from utils.generate_assets import ensure_assets
from services.db import init_db
from handlers import common, courses, promos, form

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("[START] Starting Floristry School Telegram Bot...")

    # 1. Ensure asset files (PDF catalog & Founder photo) exist
    ensure_assets(ASSETS_DIR)

    # 2. Initialize SQLite Database
    await init_db()
    logger.info("[DB] Database initialized successfully.")

    # 3. Check Bot Token
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error("[CONFIG ERROR] BOT_TOKEN is not set in .env file!")
        print("\n=======================================================")
        print("ERROR: BOT_TOKEN is not set in .env file!")
        print("=======================================================\n")
        sys.exit(1)

    # 4. Initialize Bot & Dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # 5. Include Routers
    dp.include_router(common.router)
    dp.include_router(courses.router)
    dp.include_router(promos.router)
    dp.include_router(form.router)

    # 6. Start polling
    logger.info("[POLLING] Bot is polling for updates...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("[STOP] Bot stopped.")
