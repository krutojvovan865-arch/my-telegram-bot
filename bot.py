import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8503266097:AAHYLwclZLsu8pudOw_gKQDmVyYOX_5ApPo"

# Класс состояний (этапы анкеты)
class Form(StatesGroup):
    name = State()    # Состояние: ждем имя
    age = State()     # Состояние: ждем возраст
    city = State()    # Состояние: ждем город

# Обычные кнопки
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет 👋")],
        [KeyboardButton(text="Пока 👋")]
    ],
    resize_keyboard=True
)

# Список фактов
FACTS = [
    "Осьминог имеет три сердца. 🐙",
    "Банан на самом деле является ягодой. 🍌",
    "Страусы могут бегать быстрее лошадей. 🐎",
    "Группа крови у кошек — это A, B и AB. 🐱",
    "Космос пахнет жженым сахаром и малиной. 🌌"
]

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # --- СТАРТОВЫЕ КОМАНДЫ ---
    @dp.message(Command("start"))
    async def start_command(message: types.Message):
        await message.answer("Выбери действие:", reply_markup=kb)

    @dp.message(Command("boom"))
    async def boom_command(message: types.Message):
        await message.answer("Бурмалда! 🎉")

    # --- ИНЛАЙН КНОПКИ ---
    @dp.message(Command("links"))
    async def show_links(message: types.Message):
        inline_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Наш YouTube", url="https://www.youtube.com")],
                [InlineKeyboardButton(text="Написать создателю", url="https://t.me/kegametat")]
            ]
        )
        await message.answer("Полезные ссылки:", reply_markup=inline_kb)

    @dp.message(Command("fact"))
    async def show_fact_menu(message: types.Message):
        fact_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Покажи случайный факт 🧠", callback_data="random_fact")]
            ]
        )
        await message.answer("Нажми на кнопку, чтобы узнать интересный факт!", reply_markup=fact_kb)

    @dp.callback_query(lambda c: c.data == "random_fact")
    async def process_random_fact(callback_query: types.CallbackQuery):
        random_fact = random.choice(FACTS)
        await callback_query.answer("Вот твой факт! 🧠")
        await callback_query.message.edit_text(f"🧠 Знаешь ли ты?\n{random_fact}")

    # Прямая команда для факта
    @dp.message(Command("random_fact"))
    async def direct_random_fact(message: types.Message):
        random_fact = random.choice(FACTS)
        await message.answer(f"🧠 Знаешь ли ты?\n{random_fact}")

    # --- ОБЫЧНЫЕ КНОПКИ ---
    @dp.message(lambda message: message.text == "Привет 👋")
    async def say_hello(message: types.Message):
        await message.answer("И тебе привет! Как дела?")

    @dp.message(lambda message: message.text == "Пока 👋")
    async def say_bye(message: types.Message):
        await message.answer("Пока! Возвращайся ещё!")

    # --- ЭХО ---
    @dp.message()
    async def echo_message(message: types.Message):
        await message.answer(f"Ты написал: {message.text}")

    # ==========================================
    # ⭐ МАШИНА СОСТОЯНИЙ (FSM) - АНКЕТА
    # ==========================================
    @dp.message(Command("form"))
    async def start_form(message: types.Message, state: FSMContext):
        # Начинаем анкету, переводим пользователя в состояние name
        await state.set_state(Form.name)
        await message.answer("Привет! Давай заполним анкету. Как тебя зовут?")

    @dp.message(Form.name)
    async def process_name(message: types.Message, state: FSMContext):
        # Сохраняем имя
        await state.update_data(name=message.text)
        # Переходим в состояние age
        await state.set_state(Form.age)
        await message.answer(f"Приятно познакомиться, {message.text}! Сколько тебе лет?")

    @dp.message(Form.age)
    async def process_age(message: types.Message, state: FSMContext):
        # Сохраняем возраст
        await state.update_data(age=message.text)
        # Переходим в состояние city
        await state.set_state(Form.city)
        await message.answer("Отлично! Из какого ты города?")

    @dp.message(Form.city)
    async def process_city(message: types.Message, state: FSMContext):
        # Сохраняем город
        await state.update_data(city=message.text)
        
        # Получаем все сохраненные данные
        data = await state.get_data()
        
        # Отправляем итоговое сообщение
        await message.answer(
            f"✅ Анкета заполнена!\n\n"
            f"Имя: {data['name']}\n"
            f"Возраст: {data['age']}\n"
            f"Город: {data['city']}\n\n"
            f"Спасибо!"
        )
        # Сбрасываем состояние (освобождаем память)
        await state.clear()

    print("✅ Бот слушает сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
