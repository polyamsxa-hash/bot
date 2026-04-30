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
        prompt = f"""
Ты профессиональный менеджер по продажам.

ЖЁСТКИЕ ПРАВИЛА:
- Пиши ТОЛЬКО на русском языке
- Пиши простым текстом (без таблиц, без символов, без форматирования)
- Отвечай коротко (2-3 предложения)
- Пиши как живой человек

Твоя задача — помочь клиенту и подвести к покупке.

Сообщение клиента: {message.text}
"""

        url = f"https://api.qewertyy.dev/chatgpt?prompt={prompt}"
        r = requests.get(url)

        data = r.json()
        answer = data.get("response", "")

        # чистим мусор
        if "|" in answer:
            answer = answer.split("|")[0]

        if "Support Pollinations" in answer:
            answer = answer.split("Support Pollinations")[0]

        for bad in ["#", "*"]:
            answer = answer.replace(bad, "")

        answer = answer.strip()

        await message.answer(answer)

    except Exception as e:
        print("❌ ОШИБКА:", e)
        await message.answer("Ошибка 😔")

async def main():
    print("Бот запущен 🤖")
    await dp.start_polling(bot)

asyncio.run(main())

        await message.answer(r.text)

    except Exception as e:
        print("❌ ОШИБКА:", e)
        await message.answer("Ошибка 😔")

async def main():
    print("Бот запущен 🤖")
    await dp.start_polling(bot)

asyncio.run(main())
