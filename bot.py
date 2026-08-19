import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8503266097:AAHYLwclZLsu8pudOw_gKQDmVyYOX_5ApPo"
GEMINI_API_KEY = "AQ.Ab8RN6Kp0AAFDiS6q3LKIaeMP_WKMlPlQqsanp65cAay_I_YYQ"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start_command(message: types.Message):
        await message.answer("Привет! Я ИИ-бот на Google Gemini! Спрашивай что хочешь.")

    @dp.message()
    async def ai_response(message: types.Message):
        try:
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{"parts": [{"text": message.text}]}]
            }
            response = requests.post(url, headers=headers, json=data, timeout=15)
            if response.status_code != 200:
                await message.answer(f"❌ Ошибка Google (код {response.status_code})")
                return
            answer = response.json()['candidates'][0]['content']['parts'][0]['text']
            await message.answer(answer)
        except Exception as e:
            await message.answer(f"🔥 Ошибка ИИ: {str(e)}")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
