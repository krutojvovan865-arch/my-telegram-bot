import asyncio
import random
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8503266097:AAHYLwclZLsu8pudOw_gKQDmVyYOX_5ApPo"

# КЛЮЧИ ЯНДЕКСА (с защитой + "")
YANDEX_API_KEY = "AQVN2O9Ao3RJxULmEmg-npX7M5AC1wAH2jaf3tN" + ""
FOLDER_ID = "b1gr3nt9914e976mcqjh" + ""

# Обычные кнопки
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет 👋")],
        [KeyboardButton(text="Пока 👋")]
    ],
    resize_keyboard=True
)

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start_command(message: types.Message):
        await message.answer("Привет! Я ИИ-бот. Напиши мне что-нибудь.", reply_markup=kb)

    @dp.message(Command("boom"))
    async def boom_command(message: types.Message):
        await message.answer("Бурмалда! 🎉")

    # Обычные кнопки
    @dp.message(lambda message: message.text == "Привет 👋")
    async def say_hello(message: types.Message):
        await message.answer("И тебе привет! Как дела?")

    @dp.message(lambda message: message.text == "Пока 👋")
    async def say_bye(message: types.Message):
        await message.answer("Пока! Возвращайся ещё!")

    # ==========================================
    # ⭐ ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ (YANDEXGPT) ⭐
    # ==========================================
    @dp.message()
    async def ai_response(message: types.Message):
        try:
            url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
            headers = {
                "Authorization": f"Api-Key {YANDEX_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
                "completionOptions": {"stream": False, "temperature": 0.6},
                "messages": [{"role": "user", "text": message.text}]
            }

            response = requests.post(url, headers=headers, json=data, timeout=15)

            if response.status_code != 200:
                await message.answer(f"❌ Ошибка Яндекса (код {response.status_code}):\n{response.text}")
                return

            result = response.json()
            answer = result['result']['alternatives'][0]['message']['text']
            await message.answer(answer)

        except Exception as e:
            await message.answer(f"🔥 Ошибка соединения с ИИ:\n{str(e)}")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
