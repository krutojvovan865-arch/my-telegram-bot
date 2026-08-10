import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8503266097:AAHYLwclZLsu8pudOw_gKQDmVyYOX_5ApPo"

# Создаём клавиатуру с кнопками
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
        await message.answer("Выбери действие:", reply_markup=kb)

    # Новая команда! Напиши боту /boom
    @dp.message(Command("boom"))
    async def boom_command(message: types.Message):
        await message.answer("Бурмалда! 🎉")

    @dp.message(lambda message: message.text == "Привет 👋")
    async def say_hello(message: types.Message):
        await message.answer("И тебе привет! Как дела?")

    @dp.message(lambda message: message.text == "Пока 👋")
    async def say_bye(message: types.Message):
        await message.answer("Пока! Возвращайся ещё!")

    @dp.message()
    async def echo_message(message: types.Message):
        await message.answer(f"Ты написал: {message.text}")

    print("✅ Бот слушает сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
