import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8503266097:AAHYLwclZLsu8pudOw_gKQDmVyYOX_5ApPo"

# Обычная клавиатура (Reply)
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет 👋")],
        [KeyboardButton(text="Пока 👋")]
    ],
    resize_keyboard=True
)

# ==========================================
# СПИСОК ИНТЕРЕСНЫХ ФАКТОВ
# ==========================================
FACTS = [
    "Осьминог имеет три сердца. 🐙",
    "Банан на самом деле является ягодой. 🍌",
    "Страусы могут бегать быстрее лошадей. 🐎",
    "Группа крови у кошек — это A, B и AB. 🐱",
    "Арахис на самом деле не орех, а бобовое растение. 🥜",
    "За одну минуту человек моргает около 15-20 раз. 👁️",
    "Сердце кита бьется всего 10 раз в минуту. 🐋",
    "В древнем Египте кошек считали богами. 🐈",
    "У улиток около 25 000 зубов. 🐌",
    "Космос пахнет жженым сахаром и малиной. 🌌"
]

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start_command(message: types.Message):
        await message.answer("Выбери действие:", reply_markup=kb)

    @dp.message(Command("boom"))
    async def boom_command(message: types.Message):
        await message.answer("Бурмалда! 🎉")

    # Инлайн-кнопки со ссылками (с вашим новым ником)
    @dp.message(Command("links"))
    async def show_links(message: types.Message):
        inline_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Перейти на YouTube", url="https://www.youtube.com")],
                [InlineKeyboardButton(text="Написать создателю", url="https://t.me/kegametat")]
            ]
        )
        await message.answer("Полезные ссылки:", reply_markup=inline_kb)

    # Инлайн-кнопки с выбором факта
    @dp.message(Command("fact"))
    async def show_fact_menu(message: types.Message):
        fact_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Покажи случайный факт 🧠", callback_data="random_fact")]
            ]
        )
        await message.answer("Нажми на кнопку, чтобы узнать интересный факт!", reply_markup=fact_kb)

    # Обработчик нажатия на кнопку "Покажи случайный факт"
    @dp.callback_query(lambda c: c.data == "random_fact")
    async def process_random_fact(callback_query: types.CallbackQuery):
        # Выбираем случайный факт из списка
        random_fact = random.choice(FACTS)
        await callback_query.answer("Вот твой факт! 🧠")
        await callback_query.message.edit_text(f"🧠 Знаешь ли ты?\n{random_fact}")

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
