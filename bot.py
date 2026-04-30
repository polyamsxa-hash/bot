import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
import google.generativeai as genai

# ======================
# НАСТРОЙКИ
# ======================

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("BOT_TOKEN и GEMINI_API_KEY должны быть указаны!")

# Gemini (старый, но рабочий вариант)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ======================
# ПРОМПТ (менеджер продаж)
# ======================

SYSTEM_PROMPT = """
Ты — умный, опытный и полезный ИИ-помощник менеджера по продажам техники.

Ассортимент: Apple (iPhone, MacBook, AirPods, Watch, iPad), Samsung Galaxy, PlayStation 5 + подписки, Xbox + Game Pass, Ray-Ban Meta, Dyson (фены, Airwrap, пылесосы), Dreame, бьюти-техника (стайлеры, выпрямители) и аксессуары.

Ты отвечаешь максимально полезно, естественно и по делу.

Правила ответа:
- Если клиент спрашивает о различиях моделей (например "17 про и 17 про макс отличие") — дай чёткое, понятное сравнение по ключевым параметрам (экран, батарея, камера, размер, вес, цена и т.д.).
- Если вопрос про характеристики — отвечай конкретно и кратко.
- Если менеджер пишет про сомнение клиента ("дорого", "подумаю", "есть дешевле") — предлагай 2-4 естественных вопроса в формате "или — или?" + короткую подсказку.
- Говори живым языком, как опытный коллега.
- Используй русский язык.
- Будь лаконичным: старайся не писать слишком длинные тексты.
- Если не уверен в актуальных характеристиках — скажи об этом честно.

Пример хорошего ответа:

Менеджер: 17 про и 17 про макс отличие

Ответ:
Основные отличия iPhone 17 Pro и 17 Pro Max:

• Экран: 6.3" vs 6.9" 
• Батарея: Max заметно лучше (примерно +25-30% автономности)
• Размер и вес: Pro Max тяжелее и крупнее
• Камера: почти одинаковая, но Max чуть лучше стабилизация в видео
• Цена: разница обычно 15-20 тысяч рублей

Что обычно спрашивают клиенты: нужен ли большой экран и максимальная автономность, или важнее компактность?

---

Менеджер: клиент сказал дорого

Ответ:
Классика. 

Можешь спросить:
Сейчас ты больше смотришь на цену или на то, сколько он прослужит и какие возможности даёт?

Или:
Вопрос в бюджете или сравниваешь именно 17 Pro с Pro Max?

Подсказка: Можно сразу упомянуть trade-in и рассрочку.
"""

# ======================
# ОБРАБОТЧИК
# ======================

@dp.message()
async def handler(message: types.Message):
    text = message.text.strip()

    if not text:
        await message.answer("Напиши сообщение клиента")
        return

    try:
        prompt = f"""
{SYSTEM_PROMPT}

Клиент: {text}
"""

        response = model.generate_content(prompt)
        answer = response.text.strip()

        # чистка мусора
        for bad in ["###", "*", "|"]:
            answer = answer.replace(bad, "")

        await message.answer(answer)

    except Exception as e:
        logging.error(e)
        await message.answer("Ошибка ИИ, попробуй ещё раз")

# ======================
# ЗАПУСК
# ======================

async def main():
    print("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
