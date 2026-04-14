from pyrogram import Client
from config import Config
import time

bot = Client(
    "MusicBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="bot/plugins"),
    workers=100
)

bot.start_time = time.time()
