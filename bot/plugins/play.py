import os
from pyrogram import filters, Client
from pyrogram.types import Message
from bot.youtube import get_youtube_details
from bot.call import pytgcalls
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality
from bot.strings import Strings
import bot.queue as queue_manager
from pyrogram.errors import DocumentInvalid
from config import Config
from bot.images import Images
from bot.buttons import Buttons

@Client.on_message(filters.command(["play", "vplay", "playforce", "vplayforce"]) & filters.group)
async def play_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    command = message.command[0].lower()
    is_force = "force" in command
    is_video = "v" in command
    
    # 1. Handle Telegram file playback
    if message.reply_to_message:
        reply = message.reply_to_message
        tg_file = reply.audio or reply.voice or reply.video or reply.document
        
        if tg_file:
            m = await message.reply_text(Strings.DOWNLOADING_TG_MSG)
            try:
                os.makedirs("downloads", exist_ok=True)
                file_path = await reply.download(file_name=f"downloads/{tg_file.file_id}")
                title = getattr(tg_file, 'file_name', 'Telegram File')
                
                # Check if it's a video file or if vplay was used
                if reply.video or reply.document and getattr(tg_file, 'mime_type', '').startswith('video/'):
                    is_video = True
                
                # Extract duration for Telegram files
                duration_sec = getattr(tg_file, 'duration', 0)
                from bot.youtube import _format_duration
                duration = _format_duration(duration_sec) if duration_sec else "N/A"
                artist = user_name # Fallback artist for TG files
                
                if is_force:
                    # Clear queue and stop current stream
                    queue_manager.clear_queue(chat_id)
                    try:
                        await pytgcalls.leave_call(chat_id)
                    except Exception:
                        pass
                
                if not queue_manager.is_empty(chat_id):
                    # Add to queue
                    pos = queue_manager.add_to_queue(chat_id, title, file_path, user_name, duration, artist)
                    message_text = Strings.get_added_queue_msg(title=title, pos=pos, user=user_name)
                    try:
                        await m.delete()
                        return await message.reply_photo(photo=Images.get_play_image(), caption=message_text)
                    except Exception:
                        fallback_emoji_map = {Config.SUCCESS_EMOJI_ID: "📝"}
                        return await m.edit(Strings.get_message_with_fallback(message_text, fallback_emoji_map))
                else:
                    # Play directly
                    if is_video:
                        await pytgcalls.play(chat_id, MediaStream(file_path, audio_parameters=AudioQuality.MEDIUM, video_parameters=VideoQuality.HD))
                    else:
                        await pytgcalls.play(chat_id, MediaStream(file_path, audio_parameters=AudioQuality.MEDIUM))
                    
                    # Add to queue as currently playing
                    queue_manager.add_to_queue(chat_id, title, file_path, user_name, duration, artist)
                    # For Telegram files, use the extracted duration
                    message_text = Strings.get_streaming_started_msg(title=title, duration=duration, artist=user_name, is_video=is_video)
                    try:
                        await m.delete()
                        return await message.reply_photo(photo=Images.get_play_image(), caption=message_text)
                    except Exception:
                        fallback_emoji_map = {
                            Config.PLAYING_EMOJI_ID: "🎵"
                        }
                        return await m.edit(Strings.get_message_with_fallback(message_text, fallback_emoji_map))
            except Exception as e:
                # Send custom error message to group
                try:
                    await m.delete()
                    await message.reply_text(Strings.PLAY_ERROR_MSG)
                except Exception:
                    await message.reply_text(Strings.PLAY_ERROR_MSG)
                
                # Send real error to log group
                if Config.LOG_ID:
                    try:
                        from bot.bot import bot
                        log_message = f"<blockquote>❌ **Play Error in {chat_id}**\n\n👤 User: {user_name}\n📁 File: {title}\n\n⚠️ Error:\n{str(e)}</blockquote>"
                        await bot.send_message(Config.LOG_ID, log_message)
                    except Exception as log_error:
                        print(f"Failed to send error to log group: {log_error}")

    # 2. Handle YouTube playback
    if len(message.command) < 2:
        return await message.reply_text(Strings.PLAY_PROMPT_MSG)
    
    query = " ".join(message.command[1:])
    searching_text = Strings.get_searching_msg(query)
    try:
        m = await message.reply_text(searching_text)
    except Exception:
        fallback_emoji_map = {Config.SEARCH_EMOJI_ID: "🔍"}
        m = await message.reply_text(Strings.get_message_with_fallback(searching_text, fallback_emoji_map))
    
    details, error = await get_youtube_details(query)
    if error:
        error_text = Strings.get_error_msg(error)
        try:
            return await m.edit(error_text)
        except Exception:
            fallback_emoji_map = {Config.ERROR_EMOJI_ID: "❌"}
            return await m.edit(Strings.get_message_with_fallback(error_text, fallback_emoji_map))
    
    title = details["title"]
    file_path = details["path"]
    duration = details["duration"]
    artist = details["artist"]
    url = details["url"]
    
    if is_force:
        # Clear queue and stop current stream
        queue_manager.clear_queue(chat_id)
        try:
            await pytgcalls.leave_call(chat_id)
        except Exception:
            pass

    if not queue_manager.is_empty(chat_id):
        # Add to queue
        pos = queue_manager.add_to_queue(chat_id, title, file_path, user_name, duration, artist, details.get("thumbnail"), url)
        await m.delete()
        
        # Use the updated queue added message
        message_text = Strings.get_added_queue_msg(title=title, pos=pos, user=user_name, duration=duration, url=url)
        
        # Use get_play_image for queue messages
        await message.reply_photo(
            photo=Images.get_play_image(),
            caption=message_text,
            reply_markup=Buttons.get_close_button()
        )
    else:
        # Play directly
        try:
            if is_video:
                await pytgcalls.play(chat_id, MediaStream(file_path, audio_parameters=AudioQuality.MEDIUM, video_parameters=VideoQuality.HD))
            else:
                await pytgcalls.play(chat_id, MediaStream(file_path, audio_parameters=AudioQuality.MEDIUM))
            
            # Add to queue as currently playing
            queue_manager.add_to_queue(chat_id, title, file_path, user_name, duration, artist, details.get("thumbnail"), url)
            message_text = Strings.get_streaming_started_msg(title=title, duration=duration, artist=user_name, url=url, is_video=is_video)
            await m.delete()
            
            bot_me = await client.get_me()
            bot_username = bot_me.username
            
            try:
                # Use song thumbnail for playing message
                photo = details.get("thumbnail") if details.get("thumbnail") and os.path.exists(details.get("thumbnail")) else Images.get_play_image()
                await message.reply_photo(
                    photo=photo, 
                    caption=message_text,
                    reply_markup=Buttons.get_playback_buttons(bot_username)
                )
            except Exception:
                fallback_emoji_map = {
                    Config.PLAYING_EMOJI_ID: "🎵"
                }
                fallback_msg = Strings.get_message_with_fallback(message_text, fallback_emoji_map)
                photo = details.get("thumbnail") if details.get("thumbnail") and os.path.exists(details.get("thumbnail")) else Images.get_play_image()
                await message.reply_photo(
                    photo=photo, 
                    caption=fallback_msg,
                    reply_markup=Buttons.get_playback_buttons(bot_username)
                )
        except Exception as e:
            # Send custom error message to group
            try:
                await m.delete()
                await message.reply_text(Strings.PLAY_ERROR_MSG)
            except Exception:
                await message.reply_text(Strings.PLAY_ERROR_MSG)
            
            # Send real error to log group
            if Config.LOG_ID:
                try:
                    from bot.bot import bot
                    log_message = f"<blockquote>❌ **Play Error in {chat_id}**\n\n👤 User: {user_name}\n🎵 Query: {query}\n\n⚠️ Error:\n{str(e)}</blockquote>"
                    await bot.send_message(Config.LOG_ID, log_message)
                except Exception as log_error:
                    print(f"Failed to send error to log group: {log_error}")