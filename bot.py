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
Ты помощник менеджера по онлайн-продажам.

Твои правила:
- Отвечай ТОЛЬКО на русском языке
- Пиши ПРОСТЫМ текстом без форматирования
- НЕ используй:
  - таблицы
  - символы ### 
  - звёздочки **
  - списки с тире
- Пиши как обычный человек в чате
- Кратко и по делу
- Помогай продать продукт
- Уточняй потребности клиента

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
