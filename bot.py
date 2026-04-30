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
Ты — помощник менеджера по продажам техники (Apple, Samsung, PS5, Dyson).

Твоя задача — помогать менеджеру закрывать клиентов.

ФОРМАТ ОТВЕТА:
1. Присоединение (1 строка)
2. 3–5 вопросов в формате "или — или"
3. Короткая подсказка менеджеру

ПРАВИЛА:
- Только русский язык
- Без markdown, без таблиц, без символов ** ### |
- Коротко и по делу
- Как живой менеджер
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
