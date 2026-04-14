import yt_dlp
import re
import math
import asyncio

def _format_duration(seconds):
    if seconds is None or not isinstance(seconds, (int, float)):
        return "N/A"
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds:02d}"
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02d}"

async def search_song(query):
    """
    Search for a song and get its details using yt-dlp.
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'default_search': 'ytsearch1',
        'no_warnings': True,
    }
    
    loop = asyncio.get_event_loop()
    def extract():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(query, download=False)
            
    info = await loop.run_in_executor(None, extract)
    
    if 'entries' in info:
        video = info['entries'][0]
    else:
        video = info
        
    title = video.get('title', 'Unknown')
    duration_sec = video.get('duration', 0)
    duration = _format_duration(duration_sec)
    url = video.get('webpage_url')
    video_id = video.get('id')
    artist = video.get('uploader', 'Unknown Artist')
    
    return title, duration, url, video_id, artist

async def get_youtube_details(query):
    """
    Search for YouTube video and get stream URL.
    """
    try:
        title, duration, url, video_id, artist = await search_song(query)
        
        # We still need the actual stream URL for pytgcalls
        # Using yt-dlp to get the best audio format URL
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
        }
        
        loop = asyncio.get_event_loop()
        def extract_stream():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)
        
        info = await loop.run_in_executor(None, extract_stream)
        stream_url = info.get('url')
        
        if not stream_url:
            return None, "Could not extract stream URL."
            
        from bot.thumbnail import get_thumbnail
        thumb_path = await get_thumbnail(video_id, title)
            
        return {
            "title": title, 
            "path": stream_url, 
            "duration": duration, 
            "artist": artist, 
            "thumbnail": thumb_path,
            "video_id": video_id,
            "url": url
        }, None
        
    except Exception as e:
        return None, str(e)

async def play_youtube(chat_id, query):
    # This is now kept for backward compatibility if needed, but we'll use get_youtube_details in play.py
    from pytgcalls.types import MediaStream
    from bot.call import pytgcalls
    details, error = await get_youtube_details(query)
    if error:
        return False, error
    
    await pytgcalls.play(chat_id, MediaStream(details["path"]))
    return True, details["title"]
