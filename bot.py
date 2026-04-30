from aiogram import Bot, Dispatcher, types
import asyncio
import requests

import os
BOT_TOKEN = "8769156866:AAE9oyETBI6HlDRboTzN4rDK6Dl2Y1GKVOU"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def ai_handler(message: types.Message):
    try:
        import urllib.parse
        text = urllib.parse.quote(message.text)

prompt = f"""
Ты профессиональный менеджер по продажам.

ЖЁСТКИЕ ПРАВИЛА:
- Пиши ТОЛЬКО на русском языке
- Пиши обычным текстом, как в переписке
- ЗАПРЕЩЕНО использовать:
  таблицы, символы |, ###, **, списки, Markdown
- Не делай форматирование вообще
- Пиши коротко (2-4 предложения)
- Отвечай как живой человек

Твоя задача — помочь клиенту и мягко подвести к покупке.

Сообщение клиента: {message.text}
"""

Сообщение клиента: {message.text}
"""

url = f"https://api.qewertyy.dev/chatgpt?prompt={prompt}"
r = requests.get(url)

        await message.answer(r.text)

    except Exception as e:
        print("❌ ОШИБКА:", e)
        await message.answer("Ошибка 😔")

async def main():
    print("Бот запущен 🤖")
    await dp.start_polling(bot)

asyncio.run(main())
