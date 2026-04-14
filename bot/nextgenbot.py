import aiohttp
import asyncio
import os
from config import Config

class NextGenAPI:
    def __init__(self):
        self.api_key = Config.API_KEY
        self.base_url = Config.NEXGENBOTS_API

    async def get_audio_stream(self, video_id: str):
        """
        Fetches the audio stream URL for a given video_id using NextGenBot API.
        Includes polling logic for 'downloading' status.
        Optimized for faster play by reducing sleep intervals.
        """
        url = f"{self.base_url}/song/{video_id}"
        params = {"api": self.api_key}
        
        async with aiohttp.ClientSession() as session:
            for i in range(15):  # More frequent checks
                try:
                    async with session.get(url, params=params, timeout=60) as response:
                        if response.status == 200:
                            data = await response.json()
                            if not data:
                                return {"error": "Empty response from API"}
                            
                            status = data.get("status")
                            stream_link = data.get("link")
                            
                            if status == "done" and stream_link:
                                return {"url": stream_link}
                            elif status == "downloading":
                                # Faster polling: wait less at the beginning
                                sleep_time = 2 if i < 3 else 5
                                await asyncio.sleep(sleep_time)
                                continue
                            else:
                                return {"error": f"Unexpected status: {status}"}
                        else:
                            return {"error": f"API returned status {response.status}"}
                except Exception as e:
                    return {"error": str(e)}
            
            return {"error": "Timeout waiting for NexGen API to process the song."}

nextgen_api = NextGenAPI()
