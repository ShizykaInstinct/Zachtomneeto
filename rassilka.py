from telethon import TelegramClient, events
import asyncio
import random
from telethon.tl.types import User, Chat, Channel

api_id = 123456
api_hash = "YOUR_HASH"

client = TelegramClient("userbot", api_id, api_hash)

current_message = "Авто-сообщение."
MIN_DELAY = 4 * 60
MAX_DELAY = 5.5 * 60

@client.on(events.NewMessage(pattern=r"\.message (.+)"))
async def change_message(event):
    global current_message
    current_message = event.pattern_match.group(1)
    await event.reply(f"✔ Сообщение обновлено на:\n\n{current_message}")

def is_allowed(dialog):
    e = dialog.entity
    if isinstance(e, User):
        return True
    if isinstance(e, Chat):
        return True
    if isinstance(e, Channel) and getattr(e, "megagroup", False):
        return True
    return False

async def send_to_all_chats():
    async for dialog in client.iter_dialogs():
        if not is_allowed(dialog):
            continue
        try:
            await client.send_message(dialog.id, current_message)
            print(f"Отправлено: {dialog.name}")
        except Exception as e:
            print(f"Ошибка в {dialog.name}: {e}")

async def main():
    await client.start()
    print("Юзербот запущен!")
    while True:
        await send_to_all_chats()
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        print(f"Ожидание {round(delay/60, 2)} минут...")
        await asyncio.sleep(delay)

with client:
    client.loop.run_until_complete(main())
