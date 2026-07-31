import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import init_db
from middleware import DbSessionMiddleware
from handlers import router as todo_router

async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    
    dp = Dispatcher()
    dp.message.middleware(DbSessionMiddleware())

    dp.include_router(todo_router)

    bot = Bot(token=BOT_TOKEN)
    print("Bot is up and running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

