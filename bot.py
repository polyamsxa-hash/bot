from aiogram import Bot, Dispatcher, types
import asyncio
import random

BOT_TOKEN = "8769156866:AAFJxcIEhxOrkAU6XzO6QINOLWM4u-sZ7IM"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

start_phrases = [
    "Понимаю вас",
    "Хороший вопрос",
    "Да, давайте разберёмся",
    "Конечно, помогу"
]

fallback_answers = [
    "Давайте подберём оптимальный вариант под ваш запрос. Что для вас сейчас важнее?",
    "Могу помочь разобраться и предложить лучший вариант. Расскажите чуть подробнее",
    "Подскажу лучший вариант, если уточните пару моментов",
]

@dp.message()
async def handler(message: types.Message):
    text = message.text.lower()
    start = random.choice(start_phrases)

    # ключевые темы
    if "цена" in text or "сколько" in text:
        answer = f"{start}. Скажите, на какой бюджет ориентируетесь?"

    elif "айфон" in text or "iphone" in text:
        answer = f"{start}. Могу подобрать хороший вариант с быстрой работой и камерой. Что для вас важнее — цена или функции?"

    elif "наушники" in text:
        answer = f"{start}. Есть варианты с хорошим звуком и удобством. Вам важнее звук или комфорт?"

    else:
        # универсальный умный ответ
        answer = f"{start}. {random.choice(fallback_answers)}"

    await message.answer(answer)

async def main():
    print("Бот запущен 🤖")
    await dp.start_polling(bot)

asyncio.run(main())
