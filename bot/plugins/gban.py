from pyrogram import filters, Client
from pyrogram.types import Message
from config import Config

@Client.on_message(filters.command("gban") & filters.user(Config.OWNER_ID))
async def gban_command(client: Client, message: Message):
    # Placeholder for gban logic
    await message.reply_text("User globally banned (placeholder).")

@Client.on_message(filters.command("ungban") & filters.user(Config.OWNER_ID))
async def ungban_command(client: Client, message: Message):
    # Placeholder for ungban logic
    await message.reply_text("User globally unbanned (placeholder).")

@Client.on_message(filters.command("gbannedusers") & filters.user(Config.OWNER_ID))
async def gbanned_users_command(client: Client, message: Message):
    # Placeholder for gbanned users list
    await message.reply_text("Globally banned users list (placeholder).")
