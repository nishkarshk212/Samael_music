from pyrogram import Client
from config import Config
import time

# Optimized: Increased workers and disabled storage for faster response
bot = Client(
    "MusicBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="bot/plugins"),
    workers=200,
    sleep_threshold=0,  # No delay between requests
    max_concurrent_transmissions=100  # Higher concurrency
)

bot.start_time = time.time()
