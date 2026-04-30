import asyncio
import random

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

TOKEN = "8769156866:AAFJxcIEhxOrkAU6XzO6QINOLWM4u-sZ7IM"

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(router)

# ======================
# КЛАВИАТУРЫ
# ======================

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎯 Для настроения и мотивации")],
        [KeyboardButton(text="🏢 Информация о конкурентах")],
        [KeyboardButton(text="🧠 Выявление сомнений")]
    ],
    resize_keyboard=True
)

competitors_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Саратов"), KeyboardButton(text="📍 Волгоград")],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

doubt_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💸 Дорого / Сравниваю")],
        [KeyboardButton(text="📱 Еще выбираю")],
        [KeyboardButton(text="⏳ Я откладываю покупку")],
        [KeyboardButton(text="💳 Не хочу вносить предоплату")],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

back_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⬅️ Назад в меню")]],
    resize_keyboard=True
)

# ======================
# ТЕКСТЫ
# ======================

phrases = [
    "Сегодня твой день рекордных чеков! 🍾",
    "Ты справишься! 🔥",
    "Пусть всё получится 💰"
]

DOUT_TEXT = "Сомнения — это нормально 🙂"

DORO_TEXT = "Понимаю, давай разберёмся с ценой 💸"

CHOOSE_TEXT = "Помогу выбрать 📱"

DELAY_TEXT = "Можно подождать, но условия могут измениться ⏳"

PREPAY_TEXT = "Понимаю твои переживания 💳"

SARATOV = "📍 Саратов — информация о конкурентах"
VOLGOGRAD = "📍 Волгоград — информация о конкурентах"

# ======================
# ХЕНДЛЕРЫ
# ======================

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Это рабочий бот 🥳", reply_markup=main_keyboard)


@router.message(F.text == "🎯 Для настроения и мотивации")
async def motivation(message: Message):
    await message.answer(random.choice(phrases))


@router.message(F.text == "🏢 Информация о конкурентах")
async def competitors(message: Message):
    await message.answer("Выберите город 👇", reply_markup=competitors_keyboard)


@router.message(F.text == "🧠 Выявление сомнений")
async def doubts(message: Message):
    await message.answer(DOUT_TEXT, reply_markup=doubt_keyboard)


@router.message(F.text == "⬅️ Назад в меню")
async def back(message: Message):
    await message.answer("Главное меню", reply_markup=main_keyboard)


# ======================
# СОМНЕНИЯ
# ======================

@router.message(F.text == "💸 Дорого / Сравниваю")
async def expensive(message: Message):
    await message.answer(DORO_TEXT)


@router.message(F.text == "📱 Еще выбираю")
async def choose(message: Message):
    await message.answer(CHOOSE_TEXT)


@router.message(F.text == "⏳ Я откладываю покупку")
async def delay(message: Message):
    await message.answer(DELAY_TEXT)


@router.message(F.text == "💳 Не хочу вносить предоплату")
async def prepay(message: Message):
    await message.answer(PREPAY_TEXT)


# ======================
# КОНКУРЕНТЫ
# ======================

@router.message(F.text == "📍 Саратов")
async def saratov(message: Message):
    await message.answer(SARATOV)


@router.message(F.text == "📍 Волгоград")
async def volgograd(message: Message):
    await message.answer(VOLGOGRAD)


# ======================
# ЗАПУСК
# ======================

async def main():
    print("Бот запущен 🚀")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
