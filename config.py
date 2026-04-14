import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    SESSION_STRING = os.getenv("SESSION_STRING", "")
    LOG_ID = int(os.getenv("LOG_ID", "0"))
    OWNER_ID = int(os.getenv("OWNER_ID", "8791884726"))
    OWNER_USERNAME = os.getenv("OWNER_USERNAME", "Jayden_212")
    SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "")  # Empty by default to avoid errors
    UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL", "")  # Empty by default to avoid errors
    API_KEY = os.getenv("API_KEY", "")
    NEXGENBOTS_API = os.getenv("NEXGENBOTS_API", "https://pvtz.nexgenbots.xyz")
    VIDEO_API_URL = os.getenv("VIDEO_API_URL", "https://pvtz.nexgenbots.xyz")
    
    # Other settings
    SUDO_USERS = [int(x) for x in os.getenv("SUDO_USERS", "").split(",") if x]
    if OWNER_ID and OWNER_ID not in SUDO_USERS:
        SUDO_USERS.append(OWNER_ID)
        
    # Emoji Settings
    PLAYING_EMOJI_ID = os.getenv("PLAYING_EMOJI_ID", "5427009714745517056")
    SEARCH_EMOJI_ID = os.getenv("SEARCH_EMOJI_ID", "5427009714745517056")
    PING_EMOJI_ID = os.getenv("PING_EMOJI_ID", "5427009714745517056")
    STOP_EMOJI_ID = os.getenv("STOP_EMOJI_ID", "5427009714745517056")
    QUEUE_EMOJI_ID = os.getenv("QUEUE_EMOJI_ID", "5427009714745517056")
    SKIP_EMOJI_ID = os.getenv("SKIP_EMOJI_ID", "5427009714745517056")
    ERROR_EMOJI_ID = os.getenv("ERROR_EMOJI_ID", "5427009714745517056")
    SUCCESS_EMOJI_ID = os.getenv("SUCCESS_EMOJI_ID", "5427009714745517056")
    EMOJI_PACK_IDS = [] # To store all extracted IDs from a pack

