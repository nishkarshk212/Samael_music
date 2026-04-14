from pyrogram import Client
from config import Config

assistant = Client(
    "Assistant",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.SESSION_STRING
)
