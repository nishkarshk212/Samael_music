import os
from pyrogram import filters, Client
from pyrogram.types import Message
from bot.call import pytgcalls
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality
from bot.strings import Strings
import bot.queue as queue_manager
from bot.images import Images
from bot.buttons import Buttons

LOCAL_DIR = "local_media"

@Client.on_message(filters.command("localplay") & filters.group)
async def localplay_command(client: Client, message: Message):
    chat_id = message.chat.id
    
    if not os.path.exists(LOCAL_DIR):
        os.makedirs(LOCAL_DIR)
    
    files = [f for f in os.listdir(LOCAL_DIR) if f.endswith((".mp3", ".mp4", ".mkv", ".wav", ".flac"))]
    
    if not files:
        return await message.reply_text("❌ No local files found in `local_media` directory.")
    
    if len(message.command) < 2:
        # List files
        file_list = "📂 **Local Media Files:**\n\n"
        for i, file in enumerate(files, 1):
            file_list += f"{i}. `{file}`\n"
        file_list += "\nUse `/localplay [number]` to play a file."
        return await message.reply_text(file_list)
    
    try:
        index = int(message.command[1]) - 1
        if index < 0 or index >= len(files):
            return await message.reply_text(f"❌ Invalid index. Please choose between 1 and {len(files)}.")
        
        file_name = files[index]
        file_path = os.path.join(LOCAL_DIR, file_name)
        
        # Check if it's a video file
        is_video = file_name.endswith((".mp4", ".mkv"))
        
        if not queue_manager.is_empty(chat_id):
            # Add to queue
            pos = queue_manager.add_to_queue(
                chat_id=chat_id,
                title=file_name,
                path=file_path,
                user=message.from_user.first_name,
                duration="Local",
                artist="Local Media"
            )
            message_text = Strings.get_added_queue_msg(title=file_name, pos=pos, user=message.from_user.first_name)
            return await message.reply_photo(photo=Images.get_play_image(), caption=message_text)
        else:
            # Play directly
            if is_video:
                await pytgcalls.play(chat_id, MediaStream(file_path, audio_parameters=AudioQuality.MEDIUM, video_parameters=VideoQuality.HD))
            else:
                await pytgcalls.play(chat_id, MediaStream(file_path, audio_parameters=AudioQuality.MEDIUM))
            
            # Add to queue as currently playing
            queue_manager.add_to_queue(
                chat_id=chat_id,
                title=file_name,
                path=file_path,
                user=message.from_user.first_name,
                duration="Local",
                artist="Local Media"
            )
            
            message_text = Strings.get_streaming_started_msg(title=file_name, duration="Local", artist="Local Media")
            bot_me = await client.get_me()
            return await message.reply_photo(
                photo=Images.get_play_image(),
                caption=message_text,
                reply_markup=Buttons.get_playback_buttons(bot_me.username),
                parse_mode="html"
            )
            
    except ValueError:
        return await message.reply_text("❌ Please provide a valid number.")
    except Exception as e:
        # Send custom error message to group
        try:
            await message.reply_text(Strings.PLAY_ERROR_MSG)
        except Exception:
            await message.reply_text(Strings.PLAY_ERROR_MSG)
        
        # Send real error to log group
        from config import Config
        if Config.LOG_ID:
            try:
                from bot.bot import bot
                log_message = f"<blockquote>❌ **Local Play Error in {chat_id}**\n\n👤 User: {message.from_user.first_name}\n📁 File: {file_name if 'file_name' in locals() else 'Unknown'}\n\n⚠️ Error:\n{str(e)}</blockquote>"
                await bot.send_message(Config.LOG_ID, log_message)
            except Exception as log_error:
                print(f"Failed to send error to log group: {log_error}")
