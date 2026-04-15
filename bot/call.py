from pytgcalls import PyTgCalls
from pytgcalls.types import StreamEnded, MediaStream, AudioQuality
from bot.assistant import assistant
import bot.queue as queue_manager
import os
from bot.strings import Strings
from config import Config
from pyrogram.errors import DocumentInvalid

# Optimized: Increased workers for better concurrency and faster response
pytgcalls = PyTgCalls(assistant, workers=200)

@pytgcalls.on_update()
async def on_update(client, update):
    if isinstance(update, StreamEnded):
        chat_id = update.chat_id
        # Get next item from queue
        next_track = queue_manager.pop_from_queue(chat_id)
        if next_track:
            try:
                # Play next track with medium quality
                await pytgcalls.play(
                    chat_id,
                    MediaStream(next_track["path"], audio_parameters=AudioQuality.MEDIUM)
                )
                print(f"Auto-playing next track in {chat_id}: {next_track['title']}")
                
                # Send playing message for the new track
                # Need to get the bot client to send messages
                from bot.bot import bot
                from bot.images import Images
                from bot.buttons import Buttons
                bot_me = await bot.get_me()
                bot_username = bot_me.username
                
                message_text = Strings.get_streaming_started_msg(
                    title=next_track['title'], 
                    duration=next_track.get('duration', 'N/A'), 
                    artist=next_track.get('user', 'Unknown'),
                    url=next_track.get('url')
                )
                
                try:
                    photo = next_track.get("thumbnail") if next_track.get("thumbnail") and os.path.exists(next_track["thumbnail"]) else Images.get_play_image()
                    await bot.send_photo(
                        chat_id, 
                        photo=photo, 
                        caption=message_text,
                        reply_markup=Buttons.get_playback_buttons(bot_username)
                    )
                except DocumentInvalid:
                    fallback_emoji_map = {Config.PLAYING_EMOJI_ID: "🎵"}
                    fallback_msg = Strings.get_message_with_fallback(message_text, fallback_emoji_map)
                    photo = next_track.get("thumbnail") if next_track.get("thumbnail") and os.path.exists(next_track["thumbnail"]) else Images.get_play_image()
                    await bot.send_photo(
                        chat_id, 
                        photo=photo, 
                        caption=fallback_msg,
                        reply_markup=Buttons.get_playback_buttons(bot_username)
                    )
                        
            except Exception as e:
                print(f"Error auto-playing next track in {chat_id}: {e}")
                
                # Send custom error message to group
                try:
                    from bot.bot import bot
                    await bot.send_message(chat_id, Strings.PLAY_ERROR_MSG)
                except Exception as send_error:
                    print(f"Failed to send error message to {chat_id}: {send_error}")
                
                # Send real error to log group
                if Config.LOG_ID:
                    try:
                        from bot.bot import bot
                        log_message = f"<blockquote>❌ **Auto-Play Error in {chat_id}**\n\n🎵 Track: {next_track.get('title', 'Unknown')}\n\n⚠️ Error:\n{str(e)}</blockquote>"
                        await bot.send_message(Config.LOG_ID, log_message)
                    except Exception as log_error:
                        print(f"Failed to send error to log group: {log_error}")
        else:
            # No more tracks, leave call
            try:
                await pytgcalls.leave_call(chat_id)
            except:
                pass
