import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
import google.generativeai as genai

# ======================
# НАСТРОЙКИ
# ======================

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("BOT_TOKEN и GEMINI_API_KEY должны быть указаны!")

# Gemini (старый, но рабочий вариант)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ======================
# ПРОМПТ (менеджер продаж)
# ======================

SYSTEM_PROMPT = """
Ты помощник менеджера по продажам техники.

Ассортимент:
iPhone, Samsung, PlayStation, Xbox, Dyson, наушники и аксессуары.

========================
ТВОЯ ЗАДАЧА
========================

Если сообщение — обычный вопрос:
→ отвечай коротко и понятно (по фактам)

Если сообщение — возражение клиента:
(дорого, думаю, сравниваю, позже и т.д.)

→ делай так:

1. Короткое присоединение
2. 3 вопроса в формате "или — или"
3. 1 короткая подсказка

========================
ПРАВИЛА
========================

- Только русский язык
- Без таблиц и символов типа ### * |
- Коротко и по делу
- Пиши как человек

========================
ПРИМЕР

Клиент: дорого

Ответ:

Понимаю, важно взять выгодно.

Вы сейчас сравниваете цены или выбираете модель?
Вопрос больше в бюджете или в характеристиках?
Рассматриваете экономию или лучшее качество?

Подсказка: предложи рассрочку или бонус, либо трейд-ин.
"""

# ======================
# ОБРАБОТЧИК
# ======================

@dp.message()
async def handler(message: types.Message):
    text = message.text.strip()

    if not text:
        await message.answer("Напиши сообщение клиента")
        return

    try:
        prompt = f"""
{SYSTEM_PROMPT}

Клиент: {text}
"""

        response = model.generate_content(prompt)
        answer = response.text.strip()

        # чистка мусора
        for bad in ["###", "*", "|"]:
            answer = answer.replace(bad, "")

        await message.answer(answer)

    except Exception as e:
        logging.error(e)
        await message.answer("Ошибка ИИ, попробуй ещё раз")

# ======================
# ЗАПУСК
# ======================

async def main():
    print("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
