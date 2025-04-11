import asyncio
import os
import sys
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv('local.env')


genai.configure(api_key=os.getenv('GENAI_API_KEY'))
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

bot = Bot(os.getenv("TELEGRAM_API_KEY"))
dp = Dispatcher()


@dp.message()
async def chat_with_gemini(message: Message):
    try:
        response = await asyncio.to_thread(model.generate_content, message.text)
        await message.answer(response.text.strip())
    except Exception as e:
        await message.answer(f"Ошибка при обращении к Gemini: {e}")


@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("<b>Hello!</b> I am your assistant.", parse_mode="HTML")


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
