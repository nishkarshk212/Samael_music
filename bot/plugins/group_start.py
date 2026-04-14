from pyrogram import filters, Client
from pyrogram.types import Message
from bot.strings import Strings
from bot.images import Images
from bot.buttons import Buttons
import time
from bot.bot import bot as app

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "ᴍ", "ʜ", "ᴅ"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ":"
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

@Client.on_message(filters.command("start") & filters.group)
async def group_start(client: Client, message: Message):
    try:
        # Get Bot info
        bot_me = await client.get_me()
        bot_username = bot_me.username
        bot_mention = f"[{bot_me.first_name}](tg://user?id={bot_me.id})"
        
        # Calculate uptime
        uptime = get_readable_time(int(time.time() - app.start_time))
        
        # Format message
        alive_text = Strings.ALIVE_MSG.format(
            bot_mention=bot_mention, 
            uptime=uptime
        )
        
        # Buttons
        reply_markup = Buttons.get_group_start_buttons(bot_username)
        
        # Send Photo with Fallback
        try:
            await message.reply_photo(
                photo=Images.get_start_image(),
                caption=alive_text,
                reply_markup=reply_markup
            )
        except Exception:
            await message.reply_text(alive_text, reply_markup=reply_markup)
            
    except Exception as e:
        print(f"Error in group start plugin: {e}")
