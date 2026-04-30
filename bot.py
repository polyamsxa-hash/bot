from aiogram import Bot, Dispatcher, types
import asyncio
import requests

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def ai_handler(message: types.Message):
    try:
        import urllib.parse
        text = urllib.parse.quote(message.text)

        url = f"https://text.pollinations.ai/{text}"
        r = requests.get(url)

        await message.answer(r.text)

    except Exception as e:
        print("❌ ОШИБКА:", e)
        await message.answer("Ошибка 😔")

async def main():
    print("Бот запущен 🤖")
    await dp.start_polling(bot)

asyncio.run(main())
