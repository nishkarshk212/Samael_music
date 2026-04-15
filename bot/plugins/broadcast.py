import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from bot.strings import Strings
from config import Config

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
        use_pin = "-pin" in flags
        
        if not use_user and not use_assistant:
            use_user = True
            use_assistant = True
        
        sent = 0
        failed = 0
        chats = []
        
        async for dialog in client.get_dialogs():
            if dialog.chat.type in (dialog.chat.type.SUPERGROUP, dialog.chat.type.GROUP):
                chats.append(dialog.chat.id)
        
        progress_msg = await message.reply_text(f"📢 Broadcasting to {len(chats)} chats...\n✅ Sent: 0 | ❌ Failed: 0")
        
        for i, chat_id in enumerate(chats):
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
