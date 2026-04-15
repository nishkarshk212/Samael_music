import os
import json
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from bot.strings import Strings
from config import Config

CHATS_FILE = "served_chats.json"

def load_chats():
    if os.path.exists(CHATS_FILE):
        with open(CHATS_FILE, "r") as f:
            return json.load(f)
    return []

def save_chats(chats):
    with open(CHATS_FILE, "w") as f:
        json.dump(chats, f)

def add_chat(chat_id, chat_title):
    chats = load_chats()
    chat_ids = [c["id"] for c in chats]
    if chat_id not in chat_ids:
        chats.append({"id": chat_id, "title": chat_title})
        save_chats(chats)

@Client.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID))
async def broadcast_command(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("❌ Usage: /broadcast <message> or reply to a message")
    
    try:
        args = message.command[1:]
        flags = []
        text_parts = []
        
        for arg in args:
            if arg.startswith("-"):
                flags.append(arg)
        text_parts = [arg for arg in args if not arg.startswith("-")]
        text = " ".join(text_parts)
        
        if message.reply_to_message:
            text = text if text else ""
        
        use_user = "-user" in flags
        use_assistant = "-assistant" in flags
        
        if not use_user and not use_assistant:
            use_user = True
            use_assistant = True
        
        chats = load_chats()
        
        if not chats:
            return await message.reply_text("❌ No served chats found.")
        
        sent = 0
        failed = 0
        
        progress_msg = await message.reply_text(f"📢 Broadcasting to {len(chats)} chats...\n✅ Sent: 0 | ❌ Failed: 0")
        
        for i, chat in enumerate(chats):
            chat_id = chat["id"]
            try:
                if message.reply_to_message:
                    await message.reply_to_message.copy_to(chat_id)
                else:
                    await client.send_message(chat_id, text)
                
                sent += 1
                
                if use_assistant:
                    try:
                        from bot.bot import bot
                        if message.reply_to_message:
                            await message.reply_to_message.copy_to(chat_id)
                        else:
                            await bot.send_message(chat_id, text)
                    except:
                        pass
                
                if i % 5 == 0:
                    await progress_msg.edit_text(f"📢 Broadcasting...\n✅ Sent: {sent} | ❌ Failed: {failed}\nProgress: {i+1}/{len(chats)}")
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                failed += 1
                continue
        
        result_text = f"📢 **Broadcast Complete!**\n\n✅ Sent: {sent}\n❌ Failed: {failed}\n📊 Total: {len(chats)}"
        await progress_msg.edit_text(result_text)
        
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@Client.on_message(filters.group)
async def track_chat(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        chat_title = message.chat.title or str(chat_id)
        add_chat(chat_id, chat_title)
    except:
        pass

@Client.on_message(filters.command("bcstats") & filters.user(Config.OWNER_ID))
async def bc_stats(client: Client, message: Message):
    chats = load_chats()
    await message.reply_text(f"📊 **Broadcast Stats:**\n\n📢 Total Chats: {len(chats)}")

@Client.on_message(filters.command("bcclear") & filters.user(Config.OWNER_ID))
async def bc_clear(client: Client, message: Message):
    save_chats([])
    await message.reply_text("✅ Cleared all tracked chats.")
