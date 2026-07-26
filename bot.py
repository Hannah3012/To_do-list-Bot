import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from database import init_db
import handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def main():
    init_db()
    logger.info("Database initialized.")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("add", handlers.add_todo))
    app.add_handler(CommandHandler('help', handlers.help_command))

    logger.info("Bot starting (polling mode)...")
    app.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()

