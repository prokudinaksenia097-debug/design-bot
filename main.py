import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

load_dotenv()

# ---------- НАСТРОЙКИ ----------
TOKEN = os.getenv("MAIN_BOT_TOKEN")
MANAGER_USERNAME = "@nsnsns42"
PREPAY_PERCENT = 0.15  # предоплата 15%

# ---------- УСЛУГИ ----------
SERVICES = {
    "marketplace": {
        "name": "🌇 Карточка маркетплейса",
        "price": 750,
        "description": "Продающая карточка для Wildberries, Ozon, Яндекс Маркет.\n\nЧто входит:\n• Проработанное описание\n• SEO-ключи\n• Инфографика"
    },
    "book_cover": {
        "name": "📚 Обложка книги",
        "price": 750,
        "description": "Дизайн обложки для печатной или электронной книги.\n\nЧто входит:\n• 3 варианта\n• Адаптация под формат\n• Исходники"
    },
    "banner": {
        "name": "🎨 Баннер",
        "price": 550,
        "description": "Рекламный баннер для соцсетей, сайта, наружной рекламы.\n\nЧто входит:\n• Любой размер\n• Готовые форматы"
    },
    "booklet": {
        "name": "📄 Буклет",
        "price": 850,
        "description": "Информационный буклет/брошюра.\n\nЧто входит:\n• Дизайн разворотов\n• Подготовка к печати"
    },
    "poster": {
        "name": "🖼 Плакат",
        "price": 650,
        "description": "Плакат любого формата.\n\nЧто входит:\n• Уникальный дизайн\n• Высокое разрешение"
    },
}

PRESENTATION_TEACHER = {
    "pres_teacher_10": {
        "name": "📊 Учителям (до 10 слайдов)",
        "price": 1000,
        "description": "Презентация для учителя до 10 слайдов.\n\nЧто входит:\n• Структура и дизайн\n• Исходник"
    },
    "pres_teacher_more": {
        "name": "📊 Учителям (более 10 слайдов)",
        "price": 1500,
        "description": "Презентация для учителя более 10 слайдов.\n\nЧто входит:\n• Структура и дизайн\n• Исходник"
    },
}

PRESENTATION_STUDENT = {
    "pres_student_10": {
        "name": "📊 Школьникам (до 10 слайдов)",
        "price": 300,
        "description": "Презентация для школьника до 10 слайдов.\n\nЧто входит:\n• Структура и дизайн\n• Исходник\n• Помощь с текстом"
    },
    "pres_student_more": {
        "name": "📊 Школьникам (более 10 слайдов)",
        "price": 500,
        "description": "Презентация для школьника более 10 слайдов.\n\nЧто входит:\n• Структура и дизайн\n• Исходник\n• Помощь с текстом"
    },
}

# ---------- БОТ ----------
bot = Bot(token=TOKEN)
dp = Dispatcher()


def prepay(price):
    """Считает предоплату 15% и округляет"""
    return round(price * PREPAY_PERCENT)


# ========== КЛАВИАТУРЫ ==========

def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="🛍 Услуги", callback_data="catalog")
    kb.button(text="❓ Поддержка", callback_data="support")
    kb.adjust(2)
    return kb.as_markup()


def catalog_menu():
    kb = InlineKeyboardBuilder()
    for key, srv in SERVICES.items():
        kb.button(text=f"{srv['name']} — {srv['price']} ₽", callback_data=f"service_{key}")
    kb.button(text="📊 Презентации", callback_data="presentations")
    kb.button(text="◀️ Главное меню", callback_data="main_menu")
    kb.adjust(1)
    return kb.as_markup()


def presentations_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="👩🏻‍🏫 Учителям", callback_data="pres_teacher")
    kb.button(text="👦🏻 Школьникам (1-11 класс)", callback_data="pres_student")
    kb.button(text="◀️ Назад в каталог", callback_data="catalog")
    kb.adjust(2, 1)
    return kb.as_markup()


def teacher_menu():
    kb = InlineKeyboardBuilder()
    for key, srv in PRESENTATION_TEACHER.items():
        kb.button(text=f"{srv['name']} — {srv['price']} ₽", callback_data=f"service_{key}")
    kb.button(text="◀️ Назад", callback_data="presentations")
    kb.adjust(1)
    return kb.as_markup()


def student_menu():
    kb = InlineKeyboardBuilder()
    for key, srv in PRESENTATION_STUDENT.items():
        kb.button(text=f"{srv['name']} — {srv['price']} ₽", callback_data=f"service_{key}")
    kb.button(text="◀️ Назад", callback_data="presentations")
    kb.adjust(1)
    return kb.as_markup()


def service_card(service_id, back_data="catalog"):
    """Показывает карточку услуги с кнопкой предоплаты"""
    service = None
    for d in [SERVICES, PRESENTATION_TEACHER, PRESENTATION_STUDENT]:
        if service_id in d:
            service = d[service_id]
            break

    if not service:
        return None, None

    prepay_amount = prepay(service['price'])
    text = (
        f"{service['name']}\n\n"
        f"💰 Цена: {service['price']} ₽\n"
        f"💳 Предоплата: {prepay_amount} ₽\n\n"
        f"{service['description']}"
    )

    kb = InlineKeyboardBuilder()
    kb.button(text=f"💳 Внести предоплату ({prepay_amount} ₽)", callback_data=f"prepay_{service_id}")
    kb.button(text="◀️ Назад", callback_data=back_data)
    kb.adjust(1)

    return text, kb.as_markup()


def back_only():
    kb = InlineKeyboardBuilder()
    kb.button(text="◀️ Назад в каталог", callback_data="catalog")
    return kb.as_markup()


# ========== ОБРАБОТЧИКИ ==========

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        f"👋 Привет, {message.from_user.full_name}!\n\n"
        f"Я — бот студии дизайна и презентаций.\n"
        f"Выбери, что тебя интересует:",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Выбери, что тебя интересует:",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "support")
async def support_info(callback: types.CallbackQuery):
    await callback.answer()
    text = (
        f"❓ Поддержка\n\n"
        f"По любым вопросам об услугах, оплате или заказе — пиши менеджеру:\n"
        f"@rndhelp_support_bot\n\n"
        f"Мы на связи и готовы помочь!"
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="◀️ Главное меню", callback_data="main_menu")
    await callback.message.edit_text(text, reply_markup=kb.as_markup())


@dp.callback_query(F.data == "catalog")
async def show_catalog(callback: types.CallbackQuery):
    await callback.answer()
    text = "🛍 Каталог услуг:\n\nВыбери услугу, чтобы узнать подробнее:"
    await callback.message.edit_text(text, reply_markup=catalog_menu())


@dp.callback_query(F.data == "presentations")
async def show_presentations(callback: types.CallbackQuery):
    await callback.answer()
    text = "📊 Презентации\n\nДля кого делаем?"
    await callback.message.edit_text(text, reply_markup=presentations_menu())


@dp.callback_query(F.data == "pres_teacher")
async def show_pres_teacher(callback: types.CallbackQuery):
    await callback.answer()
    text = "👩🏻‍🏫 Презентации для учителей\n\nВыбери вариант:"
    await callback.message.edit_text(text, reply_markup=teacher_menu())


@dp.callback_query(F.data == "pres_student")
async def show_pres_student(callback: types.CallbackQuery):
    await callback.answer()
    text = "👦🏻 Презентации для школьников (1-11 класс)\n\nВыбери вариант:"
    await callback.message.edit_text(text, reply_markup=student_menu())


@dp.callback_query(F.data.startswith("service_"))
async def show_service(callback: types.CallbackQuery):
    await callback.answer()
    service_id = callback.data.split("_", 1)[1]

    back_data = "catalog"
    if service_id in PRESENTATION_TEACHER:
        back_data = "pres_teacher"
    elif service_id in PRESENTATION_STUDENT:
        back_data = "pres_student"

    text, kb = service_card(service_id, back_data)
    if text is None:
        await callback.message.edit_text("Услуга не найдена", reply_markup=back_only())
        return

    await callback.message.edit_text(text, reply_markup=kb)


@dp.callback_query(F.data.startswith("prepay_"))
async def show_prepay_info(callback: types.CallbackQuery):
    await callback.answer()
    service_id = callback.data.split("_", 1)[1]

    service = None
    for d in [SERVICES, PRESENTATION_TEACHER, PRESENTATION_STUDENT]:
        if service_id in d:
            service = d[service_id]
            break

    if not service:
        await callback.answer("Ошибка")
        return

    prepay_amount = prepay(service['price'])

    text = (
        f"💳 Предоплата: {prepay_amount} ₽\n\n"
        f"Услуга: {service['name']}\n"
        f"Полная цена: {service['price']} ₽\n\n"
        f"После оплаты нажми кнопку «Я оплатил» и отправь скриншот чека менеджеру:\n"
        f"{MANAGER_USERNAME}\n\n"
        f"Не забудь указать, какая услуга тебя интересует!"
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Я оплатил", callback_data=f"paid_{service_id}")
    kb.button(text="◀️ Назад", callback_data=f"service_{service_id}")
    kb.adjust(1)

    await callback.message.edit_text(text, reply_markup=kb.as_markup())


@dp.callback_query(F.data.startswith("paid_"))
async def mark_as_paid(callback: types.CallbackQuery):
    await callback.answer()
    service_id = callback.data.split("_", 1)[1]

    service = None
    for d in [SERVICES, PRESENTATION_TEACHER, PRESENTATION_STUDENT]:
        if service_id in d:
            service = d[service_id]
            break

    if not service:
        await callback.answer("Ошибка")
        return

    prepay_amount = prepay(service['price'])

    text = (
        f"✅ Отлично!\n\n"
        f"Ты выбрал: {service['name']}\n"
        f"Предоплата: {prepay_amount} ₽\n\n"
        f"Теперь напиши менеджеру {MANAGER_USERNAME} и отправь:\n"
        f"1️⃣ Скриншот чека\n"
        f"2️⃣ Название услуги\n\n"
        f"Менеджер свяжется с тобой для уточнения деталей и выполнит заказ!\n\n"
        f"Спасибо за доверие! 🤝"
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="◀️ В каталог", callback_data="catalog")
    kb.button(text="◀️ Главное меню", callback_data="main_menu")
    kb.adjust(1)

    await callback.message.edit_text(text, reply_markup=kb.as_markup())


# ========== ЗАПУСК ==========
async def main():
    print("Бот запущен! Ожидаю сообщения...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())