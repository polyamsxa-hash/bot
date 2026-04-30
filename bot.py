from aiogram import Bot, Dispatcher, types
import asyncio
import requests

BOT_TOKEN = "8769156866:AAFJxcIEhxOrkAU6XzO6QINOLWM4u-sZ7IM"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def ai_handler(message: types.Message):
    try:
        prompt = f"""Ты менеджер по продажам. Отвечай коротко, на русском, без таблиц. Сообщение клиента: {message.text}"""

        url = f"https://api.qewertyy.dev/chatgpt?prompt={prompt}"
        r = requests.get(url, timeout=5)

        answer = ""

        try:
            data = r.json()
            answer = data.get("response", "")
        except:
            answer = ""

        # если API сломан (как сейчас)
        if not answer or "<!doctype" in r.text.lower():
            answer = "Понимаю вас, давайте подберём вариант. Скажите, что для вас важнее — цена или качество?"

        await message.answer(answer)

    except Exception as e:
        print("❌ ОШИБКА:", e)
        await message.answer("Понимаю вас, напишите что именно ищете, помогу 🙂")

async def main():
    print("Бот запущен 🤖")
    await dp.start_polling(bot)

asyncio.run(main())
