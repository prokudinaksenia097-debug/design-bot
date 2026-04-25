import asyncio
import os

MAIN_TOKEN = os.getenv("MAIN_BOT_TOKEN")
SUPPORT_TOKEN = os.getenv("SUPPORT_BOT_TOKEN")

from aiogram import Bot, Dispatcher
from main import dp as main_dp
from support_bot import dp as support_dp

main_bot = Bot(token=MAIN_TOKEN)
support_bot = Bot(token=SUPPORT_TOKEN)

async def main():
    print("Bots started!")
    await asyncio.gather(
        main_dp.start_polling(main_bot),
        support_dp.start_polling(support_bot),
    )

if __name__ == "__main__":
    asyncio.run(main())
