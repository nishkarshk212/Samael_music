from pyrogram import filters, Client
from pyrogram.types import Message
from bot.call import pytgcalls
from pytgcalls.types import MediaStream, AudioQuality
import bot.queue as queue_manager
from bot.strings import Strings
from pyrogram.errors import DocumentInvalid
from config import Config
from bot.images import Images

@Client.on_message(filters.command("skip") & filters.group)
async def skip_command(client: Client, message: Message):
    chat_id = message.chat.id
    
    # Check if anything is in queue (current track is at index 0)
    if queue_manager.is_empty(chat_id):
        return await message.reply_photo(photo=Images.get_play_image(), caption=Strings.SKIP_EMPTY_MSG)
    
    # Remove the currently playing track
    queue_manager.pop_from_queue(chat_id)
    
    # Get the next track
    next_track = queue_manager.pop_from_queue(chat_id)
    
    if next_track:
        try:
            # Add back to the beginning of queue so call.py knows it's playing
            queue_manager.add_to_queue(chat_id, next_track["title"], next_track["path"], next_track["user"])
            # Re-order to move from end to front (since add_to_queue appends)
            q = queue_manager.get_queue(chat_id)
            q.insert(0, q.pop())
            
            # Play next track with medium quality to prevent breaks
            await pytgcalls.play(chat_id, MediaStream(next_track["path"], audio_parameters=AudioQuality.MEDIUM))
            skipped_text = Strings.get_skipped_msg(next_track['title'])
            try:
                await message.reply_photo(photo=Images.get_play_image(), caption=skipped_text)
            except Exception:
                fallback_emoji_map = {Config.SKIP_EMOJI_ID: "⏭", Config.PLAYING_EMOJI_ID: "🎵"}
                await message.reply_text(Strings.get_message_with_fallback(skipped_text, fallback_emoji_map))
        except Exception as e:
            # Send custom error message to group
            try:
                await message.reply_text(Strings.PLAY_ERROR_MSG)
            except Exception:
                await message.reply_text(Strings.PLAY_ERROR_MSG)
            
            # Send real error to log group
            if Config.LOG_ID:
                try:
                    from bot.bot import bot
                    log_message = f"<blockquote>❌ **Skip Error in {chat_id}**\n\n🎵 Track: {next_track.get('title', 'Unknown')}\n\n⚠️ Error:\n{str(e)}</blockquote>"
                    await bot.send_message(Config.LOG_ID, log_message)
                except Exception as log_error:
                    print(f"Failed to send error to log group: {log_error}")
    else:
        try:
            await pytgcalls.leave_call(chat_id)
            await message.reply_photo(photo=Images.get_play_image(), caption=Strings.SKIP_NO_MORE_MSG)
        except:
            pass
