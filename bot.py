import asyncio
import random
import os  # <--- ДОБАВИЛИ ЭТО
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8503266097:AAHYLwclZLsu8pudOw_gKQDmVyYOX_5ApPo"

# Ключи теперь берутся из настроек Render, а не лежат в коде!
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("FOLDER_ID")

# Кнопки
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
        await message.answer("Я ИИ-бот! Напиши мне что-нибудь.", reply_markup=kb)

    @dp.message(Command("boom"))
    async def boom_command(message: types.Message):
        await message.answer("Бурмалда! 🎉")

    @dp.message(lambda message: message.text == "Привет 👋")
    async def say_hello(message: types.Message):
        await message.answer("И тебе привет!")

    @dp.message(lambda message: message.text == "Пока 👋")
    async def say_bye(message: types.Message):
        await message.answer("Пока!")

    # ==========================================
    # ИИ (YANDEXGPT)
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
            response = requests.post(url, headers=headers, json=data)
            answer = response.json()['result']['alternatives'][0]['message']['text']
            await message.answer(answer)
        except Exception as e:
            await message.answer("Ошибка связи с ИИ.")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
