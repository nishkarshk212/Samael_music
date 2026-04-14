import asyncio
import aiohttp
from youtubesearchpython import VideosSearch
from config import Config

def _format_duration(seconds):
    if seconds is None or not isinstance(seconds, (int, float)):
        return "N/A"
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds:02d}"
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02d}"

NEXGEN_API_URL = "https://pvtz.nexgenbots.xyz"
API_KEY = "NxGBNexGenBots53fc88"

async def get_youtube_details(query):
    """Get YouTube video details using NexGenBots API"""
    try:
        # Check if query is a URL
        is_url = query.startswith(('http://', 'https://')) or 'youtube.com' in query or 'youtu.be' in query
        
        video_id = None
        title = None
        duration = None
        artist = None
        
        if not is_url:
            # Search YouTube
            print(f"Searching for: {query}")
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
            # Extract video ID from URL
            video_url = query
            if 'youtu.be/' in query:
                video_id = query.split('youtu.be/')[-1].split('?')[0]
            elif 'v=' in query:
                video_id = query.split('v=')[-1].split('&')[0]
            else:
                return None, "Invalid YouTube URL."
        
        # Use NexGenBots API to get stream URL
        print(f"Getting stream from NexGenBots API for: {video_id}")
        
        async with aiohttp.ClientSession() as session:
            # Step 1: Request the song
            url = f"{NEXGEN_API_URL}/song/{video_id}"
            params = {"api": API_KEY}
            
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status != 200:
                    return None, f"API returned status {response.status}"
                
                data = await response.json()
                status = data.get("status")
                
                if status == "done":
                    stream_link = data.get("link")
                elif status == "downloading":
                    print("API is processing, waiting...")
                    await asyncio.sleep(10)
                    # Retry once
                    async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=60)) as response2:
                        if response2.status == 200:
                            data2 = await response2.json()
                            if data2.get("status") == "done":
                                stream_link = data2.get("link")
                            else:
                                return None, "API processing timeout. Try again."
                        else:
                            return None, f"API retry failed with status {response2.status}"
                else:
                    return None, f"Unexpected API status: {status}"
        
        if not stream_link:
            return None, "Could not get stream URL."
        
        print(f"Got stream URL: {stream_link}")
        
        # Thumbnail download in background
        if video_id:
            from bot.thumbnail import get_thumbnail
            thumbnail_task = asyncio.create_task(get_thumbnail(video_id, title))
        else:
            thumbnail_task = None
        
        return {
            "title": title,
            "path": stream_link,
            "duration": duration,
            "artist": artist,
            "thumbnail": None,
            "video_id": video_id,
            "url": video_url,
            "_thumbnail_task": thumbnail_task
        }, None
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
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
