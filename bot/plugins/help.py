from pyrogram import filters, Client
from pyrogram.types import Message
from bot.strings import Strings
from bot.images import Images
from bot.buttons import Buttons
from config import Config

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    try:
        # Support mention
        support_chat_id = str(Config.SUPPORT_CHANNEL)
        if support_chat_id.startswith("-100"):
            support_mention = f"[Support Chat](https://t.me/c/{support_chat_id[4:]}/1)"
        else:
            support_mention = f"[Support Chat](https://t.me/{support_chat_id})"
            
        help_text = Strings.HELP_MSG.format(support_mention=support_mention)
        
        await message.reply_photo(
            photo=Images.get_help_image(),
            caption=help_text,
            reply_markup=Buttons.get_help_buttons()
        )
    except Exception as e:
        print(f"Error in help command: {e}")
        await message.reply_text("Error opening help menu.")
