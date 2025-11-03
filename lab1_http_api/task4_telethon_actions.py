from telethon import TelegramClient
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

api_id = int(os.getenv("API_ID", "0"))
api_hash = os.getenv("API_HASH", "")
phone = os.getenv("PHONE", "")

client = TelegramClient("session_lab1", api_id, api_hash)

async def main():
    await client.start(phone)
    print("Connected to Telegram successfully.")

    chat_username = "nurechat"
    print(f"\nGetting list of users from chat: {chat_username}")

    try:
        participants = await client.get_participants(chat_username, limit=5)
        print("\nSample of participants:")
        for user in participants:
            print(f"- {user.first_name or ''} {user.last_name or ''} (@{user.username})")
    except Exception as e:
        print(f"Could not get participants: {e}")

    message = "Hello from Telethon demo! 👋"
    try:
        await client.send_message(chat_username, message)
        print(f"Message sent to chat {chat_username}: {message}")
    except Exception as e:
        print(f"Could not send message: {e}")

    await client.disconnect()
    print("\nSession closed.")

if __name__ == "__main__":
    asyncio.run(main())
