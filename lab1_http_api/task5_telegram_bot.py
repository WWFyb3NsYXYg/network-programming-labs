import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
import asyncio

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Welcome message"""
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="/menu"))
    await message.answer(
        "👋 Hello! I'm Lab 1 Network Programming Bot.\n"
        "Use /menu to see available commands.",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    """Show available commands"""
    await message.answer(
        "📋 Available commands:\n"
        "/menu – show this menu\n"
        "/whisper <text> – reply in lowercase\n"
        "/scream <text> – reply in uppercase"
    )

@dp.message(Command("whisper"))
async def cmd_whisper(message: Message):
    """Reply with lowercase text"""
    msg = message.text.replace("/whisper", "").strip()
    if msg:
        await message.answer(msg.lower())
    else:
        await message.answer("Please provide text after /whisper.")

@dp.message(Command("scream"))
async def cmd_scream(message: Message):
    """Reply with uppercase text"""
    msg = message.text.replace("/scream", "").strip()
    if msg:
        await message.answer(msg.upper())
    else:
        await message.answer("Please provide text after /scream.")


async def main():
    print("Lab 1 Aiogram Bot is running... Press Ctrl+C to stop.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
