import os
import asyncio
import logging
import random

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import google.generativeai as genai

# ===== НАСТРОЙКИ =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

logging.basicConfig(level=logging.INFO)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== КНОПКИ =====
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Сомнения"), KeyboardButton(text="💰 Дорого")],
        [KeyboardButton(text="🤔 Думаю"), KeyboardButton(text="📉 Сравнивает")],
        [KeyboardButton(text="🔥 Дожим"), KeyboardButton(text="🧠 ИИ помощь")]
    ],
    resize_keyboard=True
)

# ===== СКРИПТЫ =====

doubt_script = """Понимаю, важно принять правильное решение.

Вас больше останавливает цена ИЛИ вы пока выбираете модель?
Сравниваете предложения ИЛИ хотите понять, подойдёт ли этот вариант?
Сомнения из-за характеристик ИЛИ стоимости?
Вы уже почти готовы купить ИЛИ пока присматриваетесь?
"""

price_script = """Понимаю, что важно взять максимально выгодно.

Цена кажется высокой ИЛИ вы сравниваете с другими вариантами?
У нас есть трейд-ин, можно снизить стоимость.
Есть бонусная система, можно сэкономить.
Также есть гарантия лучшей цены.
"""

think_script = """Понимаю, важно всё обдумать.

Остались вопросы ИЛИ просто нужно время?
Вы выбираете между вариантами ИЛИ пока не уверены?
Что-то смущает ИЛИ просто не хотите торопиться?
"""

compare_script = """Понимаю, важно выбрать лучшее предложение.

Сравниваете по цене ИЛИ по характеристикам?
Смотрите разные магазины ИЛИ выбираете модель?
Важно дешевле ИЛИ надёжнее?
"""

close_script = """Понимаю, важно убедиться перед покупкой.

Оформляем сейчас ИЛИ остались вопросы?
Могу закрепить за вами вариант.
Если всё подходит — давайте оформим.
"""

# ===== СТАРТ =====
@dp.message()
async def handler(message: types.Message):
    text = message.text

    if text == "/start":
        await message.answer("Выбери сценарий 👇", reply_markup=keyboard)

    elif text == "📊 Сомнения":
        await message.answer(doubt_script)

    elif text == "💰 Дорого":
        await message.answer(price_script)

    elif text == "🤔 Думаю":
        await message.answer(think_script)

    elif text == "📉 Сравнивает":
        await message.answer(compare_script)

    elif text == "🔥 Дожим":
        await message.answer(close_script)

    elif text == "🧠 ИИ помощь":
        await message.answer("Отправь сообщение клиента")

    else:
        # ===== ИИ =====
        try:
            prompt = f"""
Ты помощник менеджера.
Дай короткий ответ:

1. Присоединение
2. 3 вопроса с "или"
3. Подсказка

Клиент: {text}
"""

            response = model.generate_content(prompt)
            answer = response.text.strip()

            for bad in ["###", "*", "|"]:
                answer = answer.replace(bad, "")

            await message.answer(answer)

        except Exception as e:
            logging.error(e)
            await message.answer("Ошибка ИИ")

# ===== ЗАПУСК =====
async def main():
    print("🚀 Бот запущен")
    await dp.start_polling(bot)

asyncio.run(main())
