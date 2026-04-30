from aiogram import Bot, Dispatcher, types
import asyncio
import requests

BOT_TOKEN = "8769156866:AAFJxcIEhxOrkAU6XzO6QINOLWM4u-sZ7IM"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def ai_handler(message: types.Message):
    await message.answer("я работаю")
    try:
        prompt = f"""
Ты опытный менеджер по онлайн-продажам.

ПРАВИЛА:
- Только русский язык
- Без таблиц, без символов, без форматирования
- Коротко: 2-3 предложения
- Как живой человек
- Можно задать 1 вопрос клиенту

Задача: помочь клиенту и подвести к покупке.

Сообщение клиента: {message.text}
Ответ:
"""

        url = f"https://api.qewertyy.dev/chatgpt?prompt={prompt}"
        r = requests.get(url)

        data = r.json()
        answer = data.get("response", "")

        # обрезаем мусор
        if "|" in answer:
            answer = answer.split("|")[0]

        if "Support Pollinations" in answer:
            answer = answer.split("Support Pollinations")[0]

        for bad in ["#", "*"]:
            answer = answer.replace(bad, "")

        answer = answer.strip()[:500]

        if not answer:
            answer = "Напишите подробнее, я помогу подобрать вариант 🙂"

        await message.answer(answer)

    except Exception as e:
        print("❌ ОШИБКА:", e)
        await message.answer("Ошибка 😔")

async def main():
    print("Бот запущен 🤖")
    await dp.start_polling(bot)

asyncio.run(main())
