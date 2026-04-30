import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

import google.generativeai as genai

# ====================== НАСТРОЙКИ ======================
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("BOT_TOKEN и GEMINI_API_KEY должны быть указаны в переменных окружения!")

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')   # или gemini-2.5-flash-lite для большего лимита

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class ManagerStates(StatesGroup):
    main = State()
    doubt_mode = State()


# ====================== ОБНОВЛЁННЫЙ СИСТЕМНЫЙ ПРОМПТ ======================
SYSTEM_PROMPT = """
Ты — опытный senior-помощник менеджера по продажам премиальной и геймерской техники.

Мы продаём:
- Apple (iPhone, MacBook, AirPods, Apple Watch, iPad)
- Samsung (смартфоны Galaxy, Galaxy Buds, Watch)
- PlayStation 5, игры к PS5, подписки PS Plus
- Xbox Series X/S, Game Pass
- Ray-Ban Meta (умные очки)
- Dyson (Supersonic, Airwrap, пылесосы, воздухоочистители)
- Dreame (пылесосы)
- Бьюти-техника: фены, стайлеры, выпрямители
- Наушники, зарядные устройства и аксессуары

**Не продаём** крупную технику (телевизоры, холодильники и т.п.).

Твоя задача — помогать менеджеру быстро вскрывать сомнения клиента с помощью вопросов в формате **"или — или?"**.

Когда менеджер присылает сообщение клиента, ты должен:
1. Определить настоящую причину сомнения.
2. Предложить 3–5 естественных и сильных вопросов в формате "___ или ___?".
3. Добавить короткую подсказку менеджеру (1-2 предложения максимум).

Стиль:
- Кратко, по делу, профессионально
- Только русский язык
- Вопросы должны звучать естественно, как живой менеджер
- Избегай шаблонности, делай вариации

Пример ответа:

Клиент сказал: "Дорого"

Ответ:
Вот несколько вариантов вопросов:

1. Сейчас вы в первую очередь сравниваете цену на этот iPhone с другими магазинами или смотрите на комплектацию и гарантию?
2. Вопрос сейчас именно в стоимости, или вы выбираете между iPhone и Samsung Galaxy?
3. Вы хотите взять максимально выгодно по цене или готовы рассмотреть лучшую модель с доплатой?

Подсказка: После ответа клиента можно сразу сравнить trade-in или рассрочку.
"""

# ====================== ХЭНДЛЕРЫ ======================
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "👨‍💼 ИИ-помощник менеджера по продажам техники (Apple, Samsung, PS5, Dyson и т.д.) запущен.\n\n"
        "Используй /doubt для активации режима помощи со вскрытием сомнений."
    )
    await state.set_state(ManagerStates.main)


@dp.message(Command("doubt"))
async def start_doubt_mode(message: types.Message, state: FSMContext):
    await message.answer(
        "🔍 <b>ИИ-режим вскрытия сомнений активирован</b>\n\n"
        "Просто отправляй мне сообщение клиента (или ключевые слова).\n"
        "Я буду предлагать лучшие вопросы «или — или» и подсказки.",
        parse_mode="HTML"
    )
    await state.set_state(ManagerStates.doubt_mode)


@dp.message(ManagerStates.doubt_mode)
async def process_doubt(message: types.Message, state: FSMContext):
    client_text = message.text.strip()
    
    if not client_text:
        await message.answer("Отправь, пожалуйста, что сказал клиент.")
        return

    try:
        prompt = f"Клиент сказал: \"{client_text}\""

        response = model.generate_content(
            [SYSTEM_PROMPT, prompt],
            generation_config={
                "temperature": 0.75,
                "max_output_tokens": 900,
            }
        )

        await message.answer(response.text.strip())

    except Exception as e:
        logging.error(f"Ошибка Gemini: {e}")
        await message.answer("⚠️ Ошибка при обращении к ИИ. Попробуй отправить сообщение ещё раз.")


@dp.message()
async def default_handler(message: types.Message):
    await message.answer("Для работы с сомнениями используй команду /doubt")


async def main():
    print("🚀 ИИ-помощник менеджера запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
