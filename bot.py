from aiogram import Bot, Dispatcher, types
import asyncio
import requests

BOT_TOKEN = "8769156866:AAFJxcIEhxOrkAU6XzO6QINOLWM4u-sZ7IM"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def ai_handler(message: types.Message):
    try:
        prompt = f"""Ты профессиональный менеджер по онлайн-продажам. Пиши только на русском языке, как живой человек, коротко (2–3 предложения), без таблиц, без списков, без символов и без форматирования. Всегда сначала покажи, что понял клиента, потом задай уточняющий вопрос, затем предложи простой и понятный вариант, объясняя через пользу. Не перегружай, предлагай максимум 1–2 варианта. Мягко подводи к покупке (например: оформить, подобрать, выбрать). Если клиент сомневается или говорит дорого — спокойно предложи альтернативу или уточни, что важно. Не пиши как ИИ, не используй сложные слова. Сообщение клиента: {message.text}"""

        url = f"https://api.qewertyy.dev/chatgpt?prompt={prompt}"
        r = requests.get(url, timeout=10)

        answer = ""

        # пробуем как JSON
        try:
            data = r.json()
            answer = data.get("response", "")
        except:
            answer = r.text

        # если API вернул мусор или пусто
        if not answer or len(answer) < 5:
            answer = "Понимаю вас, давайте подберём лучший вариант. Скажите, что для вас важнее — цена, качество или удобство?"

        # чистка мусора
        for bad in ["|", "#", "*"]:
            answer = answer.replace(bad, "")

        answer = answer.strip()[:400]

        await message.answer(answer)

    except Exception as e:
        print("❌ ОШИБКА:", e)
        await message.answer("Понимаю вас, напишите подробнее, что именно ищете, и я помогу 🙂")

async def main():
    print("Бот запущен 🤖")
    await dp.start_polling(bot)

asyncio.run(main())
