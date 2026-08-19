import asyncio
import os
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command


# ==============================
# НАСТРОЙКИ
# ==============================

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# Проверяем, что ключи добавлены в Render
if not TOKEN:
    raise ValueError("Не найдена переменная TELEGRAM_BOT_TOKEN")

if not OPENROUTER_API_KEY:
    raise ValueError("Не найдена переменная OPENROUTER_API_KEY")


# ==============================
# ЗАПУСК БОТА
# ==============================

async def main():

    bot = Bot(token=TOKEN)
    dp = Dispatcher()


    # ==============================
    # КОМАНДА /START
    # ==============================

    @dp.message(Command("start"))
    async def start_command(message: types.Message):

        await message.answer(
            "Привет! 👋\n\n"
            "Я ИИ-бот. Напиши мне любой вопрос, "
            "и я постараюсь на него ответить 🤖"
        )


    # ==============================
    # ОБРАБОТКА СООБЩЕНИЙ
    # ==============================

    @dp.message()
    async def ai_response(message: types.Message):

        try:

            # Если пользователь отправил не текст
            if not message.text:
                await message.answer(
                    "Пожалуйста, отправь мне текстовое сообщение."
                )
                return


            # URL OpenRouter
            url = "https://openrouter.ai/api/v1/chat/completions"


            # Заголовки
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            }


            # Запрос к ИИ
            data = {
                "model": "openrouter/free",
                "messages": [
                    {
                        "role": "user",
                        "content": message.text
                    }
                ],
                "stream": False
            }


            # Отправляем запрос
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=60
            )


            # Если OpenRouter вернул ошибку
            if response.status_code != 200:

                print("OpenRouter error:")
                print(response.text)

                await message.answer(
                    f"❌ Ошибка OpenRouter: {response.status_code}\n\n"
                    f"{response.text[:500]}"
                )

                return


            # Получаем JSON
            result = response.json()


            # Получаем ответ ИИ
            answer = result["choices"][0]["message"]["content"]


            # Отправляем ответ пользователю
            await message.answer(answer)


        except requests.exceptions.Timeout:

            await message.answer(
                "⏳ OpenRouter слишком долго отвечает. "
                "Попробуй ещё раз."
            )


        except Exception as e:

            print("Ошибка:")
            print(str(e))

            await message.answer(
                f"🔥 Ошибка ИИ:\n{str(e)}"
            )


    # ==============================
    # ЗАПУСК POLLING
    # ==============================

    print("🤖 Бот запущен!")

    await dp.start_polling(bot)


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    asyncio.run(main())
