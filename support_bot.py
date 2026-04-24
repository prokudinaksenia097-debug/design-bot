import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

load_dotenv()

# ---------- НАСТРОЙКИ ----------
TOKEN = os.getenv("SUPPORT_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7952439062"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Храним связку: сообщение админа (в чате с ботом) -> ID клиента
# Когда админ отвечает на сообщение, бот смотрит кому пересылать
admin_reply_map = {}


# ========== КЛИЕНТСКАЯ ЧАСТЬ ==========

@dp.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "👑 Привет, администратор!\n\n"
            "Когда клиент напишет в бота — ты увидишь его сообщение.\n"
            "Просто ответь на него (Reply) и клиент получит твой ответ."
        )
    else:
        await message.answer(
            "👋 Здравствуйте!\n\n"
            "Это служба поддержки студии дизайна и презентаций.\n"
            "Задайте ваш вопрос, и мы ответим в ближайшее время."
        )


@dp.message(~Command("start"))
async def handle_message(message: types.Message):
    # Сообщение от клиента
    if message.from_user.id != ADMIN_ID:
        user = message.from_user
        user_info = f"@{user.username}" if user.username else user.full_name

        # Отправляем админу
        sent_msg = await bot.send_message(
            ADMIN_ID,
            f"📩 {user_info} (ID: {user.id}):\n\n{message.text}\n\n———\nОтветь на это сообщение (Reply)"
        )

        # Запоминаем: если админ ответит на sent_msg — перешлём клиенту user.id
        admin_reply_map[sent_msg.message_id] = user.id

        # Подтверждение клиенту
        await message.answer("✅ Ваше сообщение отправлено. Поддержка ответит здесь же.")

    # Сообщение от админа — проверяем, ответил ли он на чьё-то сообщение
    else:
        if message.reply_to_message and message.reply_to_message.message_id in admin_reply_map:
            client_id = admin_reply_map[message.reply_to_message.message_id]

            await bot.send_message(
                client_id,
                f"💬 Ответ поддержки:\n\n{message.text}\n\n———\nЕсли остались вопросы — просто напишите снова!"
            )
            await message.answer("✅ Ответ отправлен клиенту.")
        else:
            await message.answer(
                "ℹ️ Это сообщение никуда не отправилось.\n"
                "Чтобы ответить клиенту — нажми Reply (Ответить) на его сообщение и напиши текст."
            )


# ========== ЗАПУСК ==========
async def main():
    print("Бот поддержки запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())