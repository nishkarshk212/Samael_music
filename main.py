import asyncio
from pyrogram import idle
from bot.bot import bot
from bot.assistant import assistant
from bot.call import pytgcalls
from bot.images import Images
from config import Config

async def main():
    print("Starting Music Bot...")
    await Images.download_all()
    await bot.start()
    print("Bot started.")
    
    print("Starting Assistant...")
    await assistant.start()
    print("Assistant started.")
    
    print("Starting PyTgCalls...")
    await pytgcalls.start()
    print("PyTgCalls started.")
    
    # Startup notifications to Log Group
    if Config.LOG_ID:
        try:
            # Bot Notification
            bot_me = await bot.get_me()
            bot_mention = f"[{bot_me.first_name}](tg://user?id={bot_me.id})"
            bot_msg = (
                f"{bot_mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :\n\n"
                f"ɪᴅ : `{bot_me.id}`\n"
                f"ɴᴀᴍᴇ : {bot_me.first_name}\n"
                f"ᴜsᴇʀɴᴀᴍᴇ : @{bot_me.username}"
            )
            await bot.send_message(Config.LOG_ID, bot_msg)
            
            # Assistant Notification
            ass_me = await assistant.get_me()
            ass_mention = f"[{ass_me.first_name}](tg://user?id={ass_me.id})"
            ass_msg = f"{ass_mention} 𝐒ᴛᴀʀᴛᴇᴅ 𝐒ᴜᴄᴄᴇssғᴜʟʟʏ..."
            await assistant.send_message(Config.LOG_ID, ass_msg)
            
        except Exception as e:
            print(f"Error sending startup notifications: {e}")

    print("Bot is now running!")
    await idle()
    
    # Graceful shutdown
    print("Stopping Bot...")
    await bot.stop()
    await assistant.stop()
    print("Stopped.")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
