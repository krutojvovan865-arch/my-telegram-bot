import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8503266097:AAHYLwclZLsu8pudOw_gKQDmVyYOX_5ApPo"
OPENROUTER_API_KEY = "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"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start_command(message: types.Message):
        await message.answer("Привет! Я ИИ-бот на OpenRouter!")

    @dp.message()
    async def ai_response(message: types.Message):
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "google/gemini-1.5-flash",
                "messages": [{"role": "user", "content": message.text}],
                "stream": False
            }
            response = requests.post(url, headers=headers, json=data, timeout=15)
            if response.status_code != 200:
                await message.answer(f"❌ Ошибка OpenRouter: {response.status_code}")
                return
            answer = response.json()['choices'][0]['message']['content']
            await message.answer(answer)
        except Exception as e:
            await message.answer(f"🔥 Ошибка ИИ: {str(e)}")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
