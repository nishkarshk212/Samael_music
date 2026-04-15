import os
import asyncio
import hashlib
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

THUMBNAIL_CACHE = {}
STREAM_CACHE = {}

async def get_youtube_details_fast(query):
    """Get YouTube video details with optimizations"""
    try:
        is_url = query.startswith(('http://', 'https://')) or 'youtube.com' in query or 'youtu.be' in query
        
        video_id = None
        title = None
        duration = None
        artist = None
        
        if not is_url:
            from youtubesearchpython import VideosSearch
            search = VideosSearch(query, limit=1)
            results = search.result()['result']
            
            if not results or len(results) == 0:
                return None, "No results found."
            
            video_data = results[0]
            video_id = video_data.get('id', '')
            video_url = f"https://youtube.com/watch?v={video_id}"
            title = video_data.get('title', 'Unknown')
            duration = video_data.get('duration', 'N/A')
            artist = video_data.get('channel', {}).get('name', 'Unknown Artist')
        else:
            video_url = query
            if 'youtu.be/' in query:
                video_id = query.split('youtu.be/')[-1].split('?')[0]
            elif 'v=' in query:
                video_id = query.split('v=')[-1].split('&')[0]
            else:
                return None, "Invalid YouTube URL."
        
        cache_key = f"{video_id}"
        if cache_key in STREAM_CACHE:
            stream_link = STREAM_CACHE[cache_key]
        else:
            import aiohttp
            NEXGEN_API_URL = "https://pvtz.nexgenbots.xyz"
            API_KEY = "NxGBNexGenBots53fc88"
            
            async with aiohttp.ClientSession() as session:
                url = f"{NEXGEN_API_URL}/song/{video_id}"
                params = {"api": API_KEY}
                
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=60)) as response:
                    if response.status != 200:
                        return None, f"API returned status {response.status}"
                    
                    data = await response.json()
                    status = data.get("status")
                    
                    if status == "done":
                        stream_link = data.get("link")
                        STREAM_CACHE[cache_key] = stream_link
                    elif status == "downloading":
                        stream_link = data.get("link")
                        STREAM_CACHE[cache_key] = stream_link
                    else:
                        return None, f"Unexpected API status: {status}"
        
        thumb_path = THUMBNAIL_CACHE.get(video_id)
        
        return {
            "title": title,
            "path": stream_link,
            "duration": duration,
            "artist": artist,
            "thumbnail": thumb_path,
            "video_id": video_id,
            "url": video_url,
        }, None
        
    except Exception as e:
        return None, f"Error: {str(e)}"

@Client.on_message(filters.command(["play", "vplay", "playforce", "vplayforce"]) & filters.group)
async def play_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    command = message.command[0].lower()
    is_force = "force" in command
    is_video = "v" in command
    
    if message.reply_to_message:
        reply = message.reply_to_message
        tg_file = reply.audio or reply.voice or reply.video or reply.document
        
        if tg_file:
            m = await message.reply_text(Strings.DOWNLOADING_TG_MSG)
            try:
                os.makedirs("downloads", exist_ok=True)
                file_path = await reply.download(file_name=f"downloads/{tg_file.file_id}")
                title = getattr(tg_file, 'file_name', 'Telegram File')
                
                if reply.video or reply.document and getattr(tg_file, 'mime_type', '').startswith('video/'):
                    is_video = True
                
                duration_sec = getattr(tg_file, 'duration', 0)
                from bot.youtube import _format_duration
                duration = _format_duration(duration_sec) if duration_sec else "N/A"
                artist = user_name
                
                if is_force:
                    queue_manager.clear_queue(chat_id)
                    try:
                        await pytgcalls.leave_call(chat_id)
                    except Exception:
                        pass
                
                if not queue_manager.is_empty(chat_id):
                    pos = queue_manager.add_to_queue(chat_id, title, file_path, user_name, duration, artist)
                    message_text = Strings.get_added_queue_msg(title=title, pos=pos, user=user_name)
                    try:
                        await m.delete()
                        return await message.reply_photo(photo=Images.get_play_image(), caption=message_text, parse_mode="html")
                    except Exception:
                        fallback_emoji_map = {Config.SUCCESS_EMOJI_ID: "📝"}
                        return await m.edit(Strings.get_message_with_fallback(message_text, fallback_emoji_map))
                else:
                    if is_video:
                        await pytgcalls.play(chat_id, MediaStream(file_path, audio_parameters=AudioQuality.MEDIUM, video_parameters=VideoQuality.HD))
                    else:
                        await pytgcalls.play(chat_id, MediaStream(file_path, audio_parameters=AudioQuality.MEDIUM))
                    
                    queue_manager.add_to_queue(chat_id, title, file_path, user_name, duration, artist)
                    message_text = Strings.get_streaming_started_msg(title=title, duration=duration, artist=user_name, is_video=is_video)
                    try:
                        await m.delete()
                        return await message.reply_photo(photo=Images.get_play_image(), caption=message_text, parse_mode="html")
                    except Exception:
                        fallback_emoji_map = {
                            Config.PLAYING_EMOJI_ID: "🎵"
                        }
                        return await m.edit(Strings.get_message_with_fallback(message_text, fallback_emoji_map))
            except Exception as e:
                try:
                    await m.delete()
                    await message.reply_text(Strings.PLAY_ERROR_MSG)
                except Exception:
                    await message.reply_text(Strings.PLAY_ERROR_MSG)
                
                if Config.LOG_ID:
                    try:
                        from bot.bot import bot
                        log_message = f"<blockquote>❌ **Play Error in {chat_id}**\n\n👤 User: {user_name}\n📁 File: {title}\n\n⚠️ Error:\n{str(e)}</blockquote>"
                        await bot.send_message(Config.LOG_ID, log_message)
                    except Exception as log_error:
                        print(f"Failed to send error to log group: {log_error}")

    if len(message.command) < 2:
        return await message.reply_text(Strings.PLAY_PROMPT_MSG)
    
    query = " ".join(message.command[1:])
    
    m = await message.reply_text(Strings.get_searching_msg(query))
    
    details, error = await get_youtube_details_fast(query)
    if error:
        try:
            await m.delete()
        except:
            pass
        error_text = Strings.get_error_msg(error)
        try:
            return await message.reply_text(error_text)
        except Exception:
            fallback_emoji_map = {Config.ERROR_EMOJI_ID: "❌"}
            return await message.reply_text(Strings.get_message_with_fallback(error_text, fallback_emoji_map))
    
    title = details["title"]
    stream_link = details["path"]
    duration = details["duration"]
    artist = details["artist"]
    url = details["url"]
    video_id = details["video_id"]
    thumb_path = details.get("thumbnail")
    
    if is_force:
        queue_manager.clear_queue(chat_id)
        try:
            await pytgcalls.leave_call(chat_id)
        except Exception:
            pass

    if not queue_manager.is_empty(chat_id):
        pos = queue_manager.add_to_queue(chat_id, title, stream_link, user_name, duration, artist, None, url)
        
        message_text = Strings.get_added_queue_msg(title=title, pos=pos, user=user_name, duration=duration, url=url)
        
        try:
            await m.delete()
        except:
            pass
        await message.reply_photo(
            photo=Images.get_play_image(),
            caption=message_text,
            reply_markup=Buttons.get_close_button()
        )
        
        if video_id:
            asyncio.create_task(_download_thumbnail_bg(video_id, title, chat_id, pos))
    else:
        try:
            if is_video:
                await pytgcalls.play(chat_id, MediaStream(stream_link, audio_parameters=AudioQuality.MEDIUM, video_parameters=VideoQuality.HD))
            else:
                await pytgcalls.play(chat_id, MediaStream(stream_link, audio_parameters=AudioQuality.MEDIUM))
            
            queue_manager.add_to_queue(chat_id, title, stream_link, user_name, duration, artist, None, url)
            message_text = Strings.get_streaming_started_msg(title=title, duration=duration, artist=user_name, url=url, is_video=is_video)
            
            bot_me = await client.get_me()
            bot_username = bot_me.username
            
            photo_to_use = thumb_path if thumb_path and os.path.exists(thumb_path) else Images.get_play_image()
            
            try:
                await m.delete()
            except:
                pass
            
            try:
                await message.reply_photo(
                    photo=photo_to_use, 
                    caption=message_text,
                    reply_markup=Buttons.get_playing_buttons(bot_username),
                    parse_mode="html"
                )
            except Exception:
                fallback_emoji_map = {
                    Config.PLAYING_EMOJI_ID: "🎵"
                }
                fallback_msg = Strings.get_message_with_fallback(message_text, fallback_emoji_map)
                await message.reply_photo(
                    photo=photo_to_use, 
                    caption=fallback_msg,
                    reply_markup=Buttons.get_playing_buttons(bot_username)
                )
            
            if video_id:
                asyncio.create_task(_download_thumbnail_bg(video_id, title, chat_id, None))
                
        except Exception as e:
            try:
                await message.reply_text(Strings.PLAY_ERROR_MSG)
            except Exception:
                await message.reply_text(Strings.PLAY_ERROR_MSG)
            
            if Config.LOG_ID:
                try:
                    from bot.bot import bot
                    log_message = f"<blockquote>❌ **Play Error in {chat_id}**\n\n👤 User: {user_name}\n🎵 Query: {query}\n\n⚠️ Error:\n{str(e)}</blockquote>"
                    await bot.send_message(Config.LOG_ID, log_message)
                except Exception as log_error:
                    print(f"Failed to send error to log group: {log_error}")

async def _download_thumbnail_bg(video_id, title, chat_id, pos):
    """Background task to download and cache thumbnail"""
    try:
        from bot.thumbnail import get_thumbnail
        thumb_path = await get_thumbnail(video_id, title)
        if thumb_path:
            THUMBNAIL_CACHE[video_id] = thumb_path
            if pos:
                queue_manager.update_queue_thumbnail(chat_id, pos, thumb_path)
    except Exception as e:
        print(f"Failed to download thumbnail: {e}")
