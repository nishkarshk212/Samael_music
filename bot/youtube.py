import yt_dlp
import re
import math
import asyncio
from functools import lru_cache

# Cache for search results (cache up to 200 searches)
@lru_cache(maxsize=200)
def _cached_search(query):
    """Synchronous cached search for faster repeated queries"""
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'default_search': 'ytsearch1',
        'no_warnings': True,
        'extract_flat': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
    
    if 'entries' in info:
        video = info['entries'][0]
    else:
        video = info
    
    return {
        'title': video.get('title', 'Unknown'),
        'duration': video.get('duration', 0),
        'url': video.get('webpage_url'),
        'video_id': video.get('id'),
        'artist': video.get('uploader', 'Unknown Artist')
    }

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
    Search for a song and get its details using yt-dlp with caching.
    """
    loop = asyncio.get_event_loop()
    # Use cached search for faster response
    result = await loop.run_in_executor(None, lambda: _cached_search(query))
    
    duration = _format_duration(result['duration'])
    
    return result['title'], duration, result['url'], result['video_id'], result['artist']

async def get_youtube_details(query):
    """
    Optimized: Search for YouTube video and get stream URL in parallel.
    Uses single yt-dlp call with optimized format extraction.
    """
    try:
        # Optimized yt-dlp options - get both info and stream in one call
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch1',
            'socket_timeout': 10,
            'retries': 2,
            'fragment_retries': 2,
            'extractor_retries': 2,
        }
        
        loop = asyncio.get_event_loop()
        def extract():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(query, download=False)
        
        info = await loop.run_in_executor(None, extract)
        
        # Handle search results
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
        stream_url = video.get('url')
        
        if not stream_url:
            return None, "Could not extract stream URL."
        
        # Run thumbnail download in parallel (don't wait for it)
        from bot.thumbnail import get_thumbnail
        thumbnail_task = asyncio.create_task(get_thumbnail(video_id, title))
        
        # Return immediately with stream_url
        return {
            "title": title, 
            "path": stream_url, 
            "duration": duration, 
            "artist": artist, 
            "thumbnail": None,  # Will be set later
            "video_id": video_id,
            "url": url,
            "_thumbnail_task": thumbnail_task  # Background task
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
