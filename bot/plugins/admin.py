from pyrogram import filters, Client
from pyrogram.types import Message
from bot.call import pytgcalls
from bot.strings import Strings
from bot.buttons import Buttons
from config import Config

@Client.on_message(filters.command("pause") & filters.group)
async def pause_command(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        await pytgcalls.pause_stream(chat_id)
        await message.reply_text("Paused ⏸")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

@Client.on_message(filters.command("resume") & filters.group)
async def resume_command(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        await pytgcalls.resume_stream(chat_id)
        await message.reply_text("Resumed ▶️")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

@Client.on_message(filters.command("player") & filters.group)
async def player_command(client: Client, message: Message):
    # This would normally show an interactive player panel
    # For now, we'll just send a placeholder message
    bot_me = await client.get_me()
    await message.reply_text(
        "Interactive Player Panel",
        reply_markup=Buttons.get_playback_buttons(bot_me.username)
    )
