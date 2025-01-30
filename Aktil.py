import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("7725771729:AAENWAle-ClInzhQPbCEJLZbAL7Ezwkdjd8")  # Telegram API Token
HF_API_KEY = os.getenv("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")  # Hugging Face API Key

bot = Bot(token=TOKEN)
dp = Dispatcher()

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
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
