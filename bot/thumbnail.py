import os
import aiohttp

async def get_thumbnail(video_id: str, title: str) -> str:
    """
    Downloads the YouTube video thumbnail and returns the local file path.
    """
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    fallback_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    
    os.makedirs("downloads/thumbnails", exist_ok=True)
    file_path = f"downloads/thumbnails/{video_id}.jpg"
    
    if os.path.exists(file_path):
        return file_path
        
    try:
        async with aiohttp.ClientSession() as session:
            # Try maxres first
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    with open(file_path, "wb") as f:
                        f.write(await resp.read())
                    return file_path
            
            # Fallback to hqdefault if maxres doesn't exist
            async with session.get(fallback_url) as resp:
                if resp.status == 200:
                    with open(file_path, "wb") as f:
                        f.write(await resp.read())
                    return file_path
                    
    except Exception as e:
        print(f"Failed to download thumbnail: {e}")
        
    return None
