from pyrogram import filters, Client
from pyrogram.types import Message
import bot.queue as queue_manager
from bot.strings import Strings
from pyrogram.errors import DocumentInvalid
from config import Config
from bot.images import Images

@Client.on_message(filters.command("queue") & filters.group)
async def queue_command(client: Client, message: Message):
    chat_id = message.chat.id
    q = queue_manager.get_queue(chat_id)
    
    if not q:
        return await message.reply_photo(photo=Images.get_queue_image(), caption=Strings.QUEUE_EMPTY)
    
    text = Strings.get_queue_header(message.chat.title)
    
    for i, track in enumerate(q):
        if i == 0:
            text += Strings.get_queue_now_playing(track['title']) + "\n"
        else:
            text += Strings.QUEUE_ITEM.format(pos=i, title=track['title'], user=track['user'])
            
    try:
        await message.reply_photo(photo=Images.get_queue_image(), caption=text)
    except Exception:
        fallback_emoji_map = {Config.QUEUE_EMOJI_ID: "📋", Config.PLAYING_EMOJI_ID: "🎵"}
        await message.reply_text(Strings.get_message_with_fallback(text, fallback_emoji_map))
