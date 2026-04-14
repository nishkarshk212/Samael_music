from pyrogram import Client
from config import Config

# Optimized: Added workers and performance settings
assistant = Client(
    "Assistant",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.SESSION_STRING,
    workers=200,
    sleep_threshold=0
)
