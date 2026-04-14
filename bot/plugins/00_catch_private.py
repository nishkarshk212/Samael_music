from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ContinuePropagation

# This handler catches ALL private messages to debug
@Client.on_message(filters.private, group=-10)
async def catch_all_private(client: Client, message: Message):
    """Catch ALL private messages for debugging"""
    print(f"🚨🚨🚨 PRIVATE MESSAGE DETECTED! 🚨🚨🚨")
    print(f"From: {message.from_user.first_name} ({message.from_user.id})")
    print(f"Chat type: {message.chat.type}")
    if message.text:
        print(f"Text: {message.text}")
    print(f"🚨🚨🚨")
    # Continue to next handler
    raise ContinuePropagation()
