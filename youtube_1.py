import asyncio
import os
import re
import json
from typing import Union
import requests
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from ..utils.database import is_on_off
from ..utils.formatters import time_to_seconds
from ANNIEMUSIC import app
import random
import logging
import aiohttp
from ANNIEMUSIC import LOGGER
from urllib.parse import urlparse


try:
    from ANNIEMUSIC import config
except ImportError:
    class config:
        YOUTUBE_IMG_URL = "https://telegra.ph/file/8ba38eca9318beb6dcede.jpg"

from brokenxapi import BrokenXAPI

# Use NexGen API from .env file
NEXGEN_API_URL = os.getenv("NEXGENBOTS_API", "https://pvtz.nexgenbots.xyz")
VIDEO_API_URL = os.getenv("VIDEO_API_URL", "https://pvtz.nexgenbots.xyz")
API_KEY = os.getenv("API_KEY")  # From your .env file


async def get_telegram_file(telegram_url: str, video_id: str, file_type: str) -> str:
    logger = LOGGER("BrokenAPI/Youtube.py")
    try:
        extension = ".webm" if file_type == "audio" else ".mkv"
        file_path = os.path.join("downloads", f"{video_id}{extension}")

        if os.path.exists(file_path):
            logger.info(f"📂 [LOCAL] File exists: {video_id}")
            return file_path

        parsed = urlparse(telegram_url)
        parts = parsed.path.strip("/").split("/")

        if len(parts) < 2:
            logger.error(f"❌ Invalid Telegram link format: {telegram_url}")
            return None

        channel_name = parts[0]
        message_id = int(parts[1])

        logger.info(f"📥 [TELEGRAM] Downloading from @{channel_name}/{message_id}")

        msg = await app.get_messages(channel_name, message_id)

        os.makedirs("downloads", exist_ok=True)
        await msg.download(file_name=file_path)

        timeout = 0
        while not os.path.exists(file_path) and timeout < 60:
            await asyncio.sleep(0.5)
            timeout += 0.5

        if os.path.exists(file_path):
            logger.info(f"✅ [TELEGRAM] Downloaded: {video_id}")
            return file_path
        else:
            logger.error(f"❌ [TELEGRAM] Timeout: {video_id}")
            return None

    except Exception as e:
        logger.error(f"❌ [TELEGRAM] Failed to download {video_id}: {e}")
        return None


async def download_song(link: str) -> str:
    """
    Download audio using ONLY NexGen API
    """
    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link
    logger = LOGGER("NexGenAPI")
    logger.info(f"🎵 [AUDIO] Starting download for: {video_id}")

    if not video_id or len(video_id) < 3:
        logger.error(f"❌ [AUDIO] Invalid video ID: {video_id}")
        return None

    os.makedirs("downloads", exist_ok=True)
    
    # Use ONLY NexGen API
    try:
        logger.info(f"🎵 [NEXGEN] Using API: {NEXGEN_API_URL}/song/{video_id}")
        async with aiohttp.ClientSession() as session:
            # Step 1: Get the stream URL
            url = f"{NEXGEN_API_URL}/song/{video_id}"
            params = {"api": API_KEY}
            
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        status = data.get("status")
                        stream_link = data.get("link")
                        
                        if status == "done" and stream_link:
                            logger.info(f"✅ [NEXGEN] Got stream link, downloading...")
                            
                            # Step 2: Download from the stream URL
                            file_path = os.path.join("downloads", f"{video_id}.m4a")
                            
                            # Check if already downloaded
                            if os.path.exists(file_path):
                                logger.info(f"✅ [NEXGEN] File already exists: {file_path}")
                                return file_path
                            
                            # Download the actual audio file
                            logger.info(f"📥 [NEXGEN] Downloading from: {stream_link}")
                            async with session.get(stream_link, timeout=aiohttp.ClientTimeout(total=300)) as stream_response:
                                if stream_response.status == 200:
                                    with open(file_path, 'wb') as f:
                                        async for chunk in stream_response.content.iter_chunked(8192):
                                            f.write(chunk)
                                    
                                    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                                        logger.info(f"✅ [NEXGEN] Successfully downloaded: {file_path}")
                                        return file_path
                                    else:
                                        logger.error(f"❌ [NEXGEN] File empty or corrupted")
                                        return None
                                else:
                                    logger.error(f"❌ [NEXGEN] Stream download failed: {stream_response.status}")
                                    return None
                        elif status == "downloading":
                            logger.info("⏳ [NEXGEN] Still processing, waiting...")
                            await asyncio.sleep(5)
                            # Retry once
                            return await download_song(link)
                        else:
                            logger.warning(f"⚠️ [NEXGEN] Unexpected status: {status}")
                    else:
                        logger.warning(f"⚠️ [NEXGEN] Empty response")
                else:
                    logger.warning(f"⚠️ [NEXGEN] API returned status {response.status}")
    except Exception as api_error:
        logger.error(f"❌ [NEXGEN] Failed: {api_error}")
        import traceback
        traceback.print_exc()
        return None


async def download_video(link: str) -> str:
    """
    Download video using ONLY NexGen API
    """
    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link
    logger = LOGGER("NexGenAPI")
    logger.info(f"🎥 [VIDEO] Starting download for: {video_id}")

    if not video_id or len(video_id) < 3:
        logger.error(f"❌ [VIDEO] Invalid video ID: {video_id}")
        return None

    os.makedirs("downloads", exist_ok=True)
    
    # Use ONLY NexGen API
    try:
        logger.info(f"🎥 [NEXGEN] Using API: {VIDEO_API_URL}/stream/{video_id}")
        async with aiohttp.ClientSession() as session:
            url = f"{VIDEO_API_URL}/stream/{video_id}"
            params = {"api": API_KEY}
            
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        status = data.get("status")
                        if status == "downloading":
                            logger.info("✅ [NEXGEN] Video download started, waiting...")
                            await asyncio.sleep(10)
                        elif status == "done":
                            logger.info("✅ [NEXGEN] Video file already downloaded!")
                        
                        # Check if file exists
                        file_path = os.path.join("downloads", f"{video_id}.mp4")
                        if os.path.exists(file_path):
                            logger.info(f"✅ [NEXGEN] Video file found: {file_path}")
                            return file_path
                    else:
                        logger.warning(f"⚠️ [NEXGEN] Empty response")
                else:
                    logger.warning(f"⚠️ [NEXGEN] API returned status {response.status}")
    except Exception as api_error:
        logger.error(f"❌ [NEXGEN] Failed: {api_error}")
        return None


async def check_file_size(link):
    async def get_format_info(link):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-J",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            print(f'Error:\n{stderr.decode()}')
            return None
        return json.loads(stdout.decode())

    def parse_size(formats):
        total_size = 0
        for format in formats:
            if 'filesize' in format:
                total_size += format['filesize']
        return total_size

    info = await get_format_info(link)
    if info is None:
        return None

    formats = info.get('formats', [])
    if not formats:
        print("No formats found.")
        return None

    total_size = parse_size(formats)
    return total_size


async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
            return out.decode("utf-8")
        else:
            return errorz.decode("utf-8")
    return out.decode("utf-8")


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset: entity.offset + entity.length]
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
            
        # Updated to use YoutubeSearch
        try:
            results = YoutubeSearch(link, max_results=1).to_dict()
            if not results:
                return None, None, None, None, None
            
            result = results[0]
            title = result.get("title", "Unknown")
            duration_min = result.get("duration", "00:00")
            thumbnail = result.get("thumbnails", [""])[0]
            vidid = result.get("id")
            duration_sec = int(time_to_seconds(duration_min)) if duration_min else 0
            
            return title, duration_min, duration_sec, thumbnail, vidid
        except:
            return None, None, None, None, None

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = YoutubeSearch(link, max_results=1).to_dict()
            if results:
                return results[0].get("title")
        except:
            return None

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = YoutubeSearch(link, max_results=1).to_dict()
            if results:
                return results[0].get("duration")
        except:
            return None

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = YoutubeSearch(link, max_results=1).to_dict()
            if results:
                return results[0].get("thumbnails", [""])[0]
        except:
            return None

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            downloaded_file = await download_video(link)
            if downloaded_file:
                return 1, downloaded_file
            else:
                return 0, "Video download failed"
        except Exception as e:
            return 0, f"Video download error: {e}"

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        playlist = await shell_cmd(
            f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
        )
        try:
            result = [key for key in playlist.split("\n") if key]
        except:
            result = []
        return result

    # --- UPDATED TRACK METHOD USING youtube_search ---
    async def track(self, link: str, videoid: Union[bool, str] = None):
        logger = LOGGER("BrokenXAPI") 
        try:
            if videoid:
                link = self.base + link

            if "&" in link:
                link = link.split("&")[0]

            # Using YoutubeSearch as requested
            # Since YoutubeSearch is synchronous, we can run it directly or in executor. 
            # For simplicity and given it's fast, running directly here.
            results = YoutubeSearch(link, max_results=1).to_dict()
            
            print(f"YoutubeSearch Results: {results}")

            if not results:
                logger.error(f"❌ No results found for: {link}")
                return None, None

            # Get the first result
            result = results[0]

            title = result.get("title", "Unknown Title")
            duration_min = result.get("duration", "00:00")
            vidid = result.get("id")
            
            # YoutubeSearch returns suffix like '/watch?v=...', we need full link
            url_suffix = result.get("url_suffix", "")
            yturl = f"https://www.youtube.com{url_suffix}"

            # Handle Thumbnails (YoutubeSearch returns a list of strings usually)
            thumbnails = result.get("thumbnails", [])
            if thumbnails and isinstance(thumbnails, list):
                thumbnail = thumbnails[0].split("?")[0]
            elif isinstance(thumbnails, str):
                thumbnail = thumbnails
            else:
                thumbnail = config.YOUTUBE_IMG_URL

            track_details = {
                "title": title,
                "link": yturl,
                "vidid": vidid,
                "duration_min": duration_min,
                "thumb": thumbnail,
            }

            return track_details, vidid

        except Exception as e:
            LOGGER("BrokenAPI/Youtube.py").error(f"❌ Track fetch failed: {e}")
            import traceback
            traceback.print_exc()
            return None, None

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        ytdl_opts = {"quiet": True}
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    if "dash" not in str(format["format"]).lower():
                        formats_available.append(
                            {
                                "format": format["format"],
                                "filesize": format.get("filesize"),
                                "format_id": format["format_id"],
                                "ext": format["ext"],
                                "format_note": format["format_note"],
                                "yturl": link,
                            }
                        )
                except:
                    continue
        return formats_available, link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        # Updated slider to use YoutubeSearch (gets 10 results by default roughly)
        try:
            results = YoutubeSearch(link, max_results=10).to_dict()
            
            if not results or len(results) <= query_type:
                return None, None, None, None

            item = results[query_type]
            
            title = item.get("title")
            duration_min = item.get("duration")
            vidid = item.get("id")
            
            thumbnails = item.get("thumbnails", [])
            if thumbnails and isinstance(thumbnails, list):
                thumbnail = thumbnails[0].split("?")[0]
            else:
                thumbnail = ""
                
            return title, duration_min, thumbnail, vidid
        except Exception as e:
            print(f"Slider Error: {e}")
            return None, None, None, None

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link

        try:
            if video:
                downloaded_file = await download_video(link)
                if downloaded_file:
                    return downloaded_file, True
                else:
                    return None, False
            else:
                downloaded_file = await download_song(link)
                if downloaded_file:
                    return downloaded_file, True
                else:
                    return None, False

        except Exception as e:
            logger = LOGGER("BrokenAPI/Youtube.py")
            logger.error(f"❌ Download failed: {e}")
            return None, False
