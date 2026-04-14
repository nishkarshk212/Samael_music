import aiohttp
import asyncio
import yt_dlp
from config import Config

def _format_duration(seconds):
    if seconds is None or not isinstance(seconds, (int, float)):
        return "N/A"
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds:02d}"
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02d}"

async def get_youtube_details(query):
    """Get YouTube video details using yt-dlp"""
    try:
        # Check if query is a URL
        is_url = query.startswith(('http://', 'https://')) or 'youtube.com' in query or 'youtu.be' in query
        
        if not is_url:
            # Search YouTube
            search_query = f"ytsearch1:{query}"
        else:
            search_query = query
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bestaudio/best',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            
            # If searching, get first result
            if not is_url:
                if not info or 'entries' not in info or not info['entries']:
                    return None, "No results found."
                info = info['entries'][0]
            
            title = info.get('title', "Unknown")
            duration_sec = info.get('duration', 0)
            duration = _format_duration(duration_sec)
            video_id = info.get('id', "")
            artist = info.get('uploader', "Unknown Artist")
            url = info.get('webpage_url', f"https://youtube.com/watch?v={video_id}")
            stream_url = info.get('url')
            
            if not stream_url:
                return None, "Could not get stream URL."
            
            # Thumbnail download in background
            from bot.thumbnail import get_thumbnail
            thumbnail_task = asyncio.create_task(get_thumbnail(video_id, title))
            
            return {
                "title": title,
                "path": stream_url,
                "duration": duration,
                "artist": artist,
                "thumbnail": None,
                "video_id": video_id,
                "url": url,
                "_thumbnail_task": thumbnail_task
            }, None
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None, f"Error: {str(e)}"

async def play_youtube(chat_id, query):
    from pytgcalls.types import MediaStream
    from bot.call import pytgcalls
    details, error = await get_youtube_details(query)
    if error:
        return False, error
    
    await pytgcalls.play(chat_id, MediaStream(details["path"]))
    return True, details["title"]
