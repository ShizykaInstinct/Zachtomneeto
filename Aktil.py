import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv  # Импортируем библиотеку для работы с .env

# Загружаем переменные окружения из файла .env (если он существует)
load_dotenv()

# Получаем токены из переменных окружения
TOKEN = os.getenv("7725771729:AAENWAle-ClInzhQPbCEJLZbAL7Ezwkdjd8")  # Токен Telegram API
HF_API_KEY = os.getenv("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")  # Токен Hugging Face API

if not TOKEN or not HF_API_KEY:
    raise ValueError("Telegram token or Hugging Face API key not found. Make sure to set them in environment variables or .env file.")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Функция для отправки запроса к Hugging Face
def chat_with_ai(text):
    url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": text}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return "Ошибка: модель не отвечает."

@dp.message()
async def message_handler(message: types.Message):
    reply = chat_with_ai(message.text)
    await message.answer(reply)

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
