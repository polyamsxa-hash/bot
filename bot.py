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
Ты опытный менеджер по онлайн-продажам.

ТВОЯ ЦЕЛЬ:
помочь клиенту и мягко привести его к покупке.

СТРОГИЕ ПРАВИЛА:
- Пиши только на русском языке
- Пиши простым текстом, как в чате (без таблиц, без символов, без оформления)
- Не используй списки, markdown, знаки |, #, *
- Пиши коротко: 2–3 предложения
- Не пиши лишнего и не уходи в длинные объяснения

СТИЛЬ:
- Вежливый, спокойный, уверенный
- Как живой менеджер, а не робот
- Можно задавать 1 уточняющий вопрос

ПРОДАЖИ:
- Выявляй потребность клиента
- Подсказывай лучший вариант
- Легко подталкивай к покупке (без давления)

ЗАПРЕЩЕНО:
- Делать таблицы
- Делать длинные сравнения
- Писать “как ИИ” или объяснять очевидное

Сообщение клиента: {message.text}

Ответ:
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
