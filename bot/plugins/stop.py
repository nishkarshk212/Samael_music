from pyrogram import filters, Client
from pyrogram.types import Message
from bot.call import pytgcalls
import bot.queue as queue_manager
from bot.strings import Strings
from pyrogram.errors import DocumentInvalid
from config import Config
from bot.images import Images

@Client.on_message(filters.command("stop") & filters.group)
async def stop_command(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        # Clear the queue first
        queue_manager.clear_queue(chat_id)
        # Leave the call
        await pytgcalls.leave_call(chat_id)
        stop_text = Strings.get_stop_msg()
        try:
            await message.reply_photo(photo=Images.get_play_image(), caption=stop_text)
        except Exception:
            fallback_emoji_map = {Config.STOP_EMOJI_ID: "⏹"}
            await message.reply_text(Strings.get_message_with_fallback(stop_text, fallback_emoji_map))
    except Exception as e:
        error_text = Strings.get_error_msg(str(e))
        try:
            await message.reply_text(error_text)
        except Exception:
            fallback_emoji_map = {Config.ERROR_EMOJI_ID: "❌"}
            await message.reply_text(Strings.get_message_with_fallback(error_text, fallback_emoji_map))
