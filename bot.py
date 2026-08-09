import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8503266097:AAHYLwclZLsu8pudOw_gKQDmVyYOX_5ApPo"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start_command(message: types.Message):
        await message.answer("Привет! Я бот, работающий на Render!")

    @dp.message()
    async def echo_message(message: types.Message):
        await message.answer(f"Ты написал: {message.text}")

    print("✅ Бот слушает сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
