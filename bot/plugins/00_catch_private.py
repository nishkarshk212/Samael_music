from pyrogram import filters, Client
from pyrogram.types import Message
from bot.strings import Strings
from config import Config
from bot.images import Images
from bot.buttons import Buttons
import traceback

# This handler catches ALL private messages and handles /start
@Client.on_message(filters.private, group=-10)
async def catch_all_private(client: Client, message: Message):
    """Catch ALL private messages and handle /start"""
    print(f"🚨🚨🚨 PRIVATE MESSAGE DETECTED! 🚨🚨🚨")
    print(f"From: {message.from_user.first_name} ({message.from_user.id})")
    print(f"Chat type: {message.chat.type}")
    if message.text:
        print(f"Text: {message.text}")
    print(f"🚨🚨🚨")
    
    # Check if it's a /start command
    if message.text and (message.text.lower() == '/start' or message.text.lower().startswith('/start ')):
        print(f"✅✅✅ HANDLING /start COMMAND ✅✅✅")
        try:
            user_id = message.from_user.id
            user_name = message.from_user.first_name or "User"
            
            # Get Bot info
            bot_me = await client.get_me()
            bot_username = bot_me.username
            bot_name = bot_me.first_name
            
            # Simple owner mention
            owner_mention = f"tg://user?id={Config.OWNER_ID}"
            
            # Format message
            start_text = Strings.PRIVATE_START_MSG.format(
                user=f"[{user_name}](tg://user?id={user_id})", 
                bot_name=f"[{bot_name}](tg://user?id={bot_me.id})",
                owner=f"[Owner]({owner_mention})"
            )
            
            # Get buttons
            try:
                reply_markup = Buttons.get_private_start_buttons(bot_username)
            except Exception as e:
                print(f"⚠️ Error generating buttons: {e}")
                reply_markup = None
            
            # Try sending photo first, fallback to text
            try:
                photo = Images.get_start_image()
                await message.reply_photo(
                    photo=photo,
                    caption=start_text,
                    reply_markup=reply_markup
                )
                print(f"✅ Start message (photo) sent to {user_name}")
            except Exception as e:
                print(f"⚠️ Photo send failed, using text: {e}")
                try:
                    await message.reply_text(
                        start_text,
                        reply_markup=reply_markup,
                        disable_web_page_preview=True
                    )
                    print(f"✅ Start message (text) sent to {user_name}")
                except Exception as e2:
                    print(f"❌ Text send also failed: {e2}")
                    await message.reply_text("👋 Welcome! Use /help to see commands.")
        except Exception as e:
            print(f"❌ Critical error in /start handler: {e}")
            traceback.print_exc()
            try:
                await message.reply_text("👋 Welcome! Something went wrong. Try /help")
            except:
                pass
