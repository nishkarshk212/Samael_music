from pyrogram import filters, Client
from pyrogram.types import Message
from bot.strings import Strings
from config import Config
from bot.images import Images
from bot.buttons import Buttons

@Client.on_message(filters.command("start") & filters.private)
async def private_start(client: Client, message: Message):
    try:
        # Get Bot info
        bot_me = await client.get_me()
        bot_username = bot_me.username
        bot_name = f"[{bot_me.first_name}](tg://user?id={bot_me.id})"
        
        # Get User info
        user_name = message.from_user.first_name if message.from_user else "User"
        user_id = message.from_user.id if message.from_user else message.chat.id
        user_mention = f"[{user_name}](tg://user?id={user_id})"
        
        # Get Owner info
        owner_id = Config.OWNER_ID
        owner_mention = "[Unknown](https://t.me/telegram)"
        if owner_id:
            try:
                owner_user = await client.get_users(owner_id)
                owner_mention = f"[{owner_user.first_name}](tg://user?id={owner_id})"
            except:
                owner_mention = f"[Owner](tg://user?id={owner_id})"

        # Format message
        start_text = Strings.PRIVATE_START_MSG.format(
            user=user_mention, 
            bot_name=bot_name,
            owner=owner_mention
        )
        
        # Buttons
        reply_markup = Buttons.get_private_start_buttons(bot_username)
        
        # Send Photo with Fallback
        try:
            await message.reply_photo(
                photo=Images.get_start_image(),
                caption=start_text,
                reply_markup=reply_markup
            )
        except Exception:
            await message.reply_text(start_text, reply_markup=reply_markup)
            
    except Exception as e:
        print(f"Critical error in private start plugin: {e}")
        import traceback
        traceback.print_exc()
