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

        url = f"https://api.qewertyy.dev/chatgpt?prompt={text}"
r = requests.get(url)

data = r.json()
await message.answer(data["response"])

    except Exception as e:
        print("❌ ОШИБКА:", e)
        await message.answer("Ошибка 😔")

async def main():
    print("Бот запущен 🤖")
    await dp.start_polling(bot)

asyncio.run(main())
