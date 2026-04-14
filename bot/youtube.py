import aiohttp
import asyncio
import re
from functools import lru_cache
from config import Config

# Cache for search results (cache up to 200 searches)
@lru_cache(maxsize=200)
def _cached_search(query):
    """Return cached query - actual search is async now"""
    return None

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
    Search for a song using NexGenBots API.
    Fast, no bot detection, no cookies needed.
    """
    try:
        api_url = f"{Config.NEXGENBOTS_API}/api/search"
        params = {
            "query": query,
            "api_key": Config.API_KEY
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("status") == "success" and data.get("results"):
                        result = data["results"][0]
                        return (
                            result.get("title", "Unknown"),
                            result.get("duration", "N/A"),
                            result.get("url", ""),
                            result.get("id", ""),
                            result.get("artist", "Unknown Artist")
                        )
        
        # Fallback: return empty if API fails
        return "Unknown", "N/A", "", "", "Unknown Artist"
    except Exception as e:
        print(f"Search error: {e}")
        return "Unknown", "N/A", "", "", "Unknown Artist"

async def get_youtube_details(query):
    """
    Get YouTube video details and stream URL using NexGenBots API.
    No cookies needed, fast response, no bot detection.
    """
    try:
        # Use NexGenBots API to get stream URL
        api_url = f"{Config.NEXGENBOTS_API}/api/play"
        params = {
            "query": query,
            "api_key": Config.API_KEY
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, timeout=15) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("status") == "success":
                        title = data.get("title", "Unknown")
                        stream_url = data.get("url") or data.get("stream_url")
                        duration_sec = data.get("duration", 0)
                        duration = _format_duration(duration_sec)
                        video_id = data.get("id", "")
                        artist = data.get("artist", "Unknown Artist")
                        url = data.get("webpage_url") or f"https://youtube.com/watch?v={video_id}"
                        
                        if not stream_url:
                            return None, "Could not get stream URL from API."
                        
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
        
        return None, "API request failed. Please try again."
        
    except Exception as e:
        return None, f"Error: {str(e)}"

async def play_youtube(chat_id, query):
    # This is now kept for backward compatibility if needed, but we'll use get_youtube_details in play.py
    from pytgcalls.types import MediaStream
    from bot.call import pytgcalls
    details, error = await get_youtube_details(query)
    if error:
        return False, error
    
    await pytgcalls.play(chat_id, MediaStream(details["path"]))
    return True, details["title"]
