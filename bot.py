import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Токены из .env
MAIN_TOKEN = os.getenv("MAIN_BOT_TOKEN")
SUPPORT_TOKEN = os.getenv("SUPPORT_BOT_TOKEN")

# Запускаем оба бота
async def main():
    from main import dp as main_dp, bot as main_bot
    from support_bot import dp as support_dp, bot as support_bot

    # Подменяем токены на те, что из .env
    main_bot.token = MAIN_TOKEN
    support_bot.token = SUPPORT_TOKEN

    print("Оба бота запущены!")

    await asyncio.gather(
        main_dp.start_polling(main_bot),
        support_dp.start_polling(support_bot),
    )


if __name__ == "__main__":
    asyncio.run(main())
    