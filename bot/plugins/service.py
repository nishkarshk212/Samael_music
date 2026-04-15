from pyrogram import filters, Client
from pyrogram.types import Message
from bot.strings import Strings
from bot.images import Images
from bot.buttons import Buttons
import bot.queue as queue_manager
from bot.call import pytgcalls
import time
from bot.bot import bot as app
from config import Config
import json
import os

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

CHATS_FILE = "served_chats.json"

def load_chats():
    if os.path.exists(CHATS_FILE):
        with open(CHATS_FILE, "r") as f:
            return json.load(f)
    return []

def save_chats(chats):
    with open(CHATS_FILE, "w") as f:
        json.dump(chats, f)

def add_chat(chat_id, chat_title):
    chats = load_chats()
    chat_ids = [c["id"] for c in chats]
    if chat_id not in chat_ids:
        chats.append({"id": chat_id, "title": chat_title})
        save_chats(chats)
        return True
    return False

@Client.on_message(filters.new_chat_members)
async def welcome_handler(client: Client, message: Message):
    for member in message.new_chat_members:
        bot_me = await client.get_me()
        if member.id == bot_me.id:
            chat_id = message.chat.id
            chat_title = message.chat.title or "Private Chat"
            
            is_new = add_chat(chat_id, chat_title)
            
            uptime = get_readable_time(int(time.time() - app.start_time))
            bot_username = bot_me.username
            bot_mention = f"[{bot_me.first_name}](tg://user?id={bot_me.id})"
            alive_text = Strings.ALIVE_MSG.format(bot_mention=bot_mention, uptime=uptime)
            
            reply_markup = Buttons.get_group_start_buttons(bot_username)
            
            try:
                await message.reply_photo(
                    photo=Images.get_start_image(), 
                    caption=alive_text,
                    reply_markup=reply_markup
                )
            except Exception:
                await message.reply_text(alive_text, reply_markup=reply_markup)
            
            if Config.LOG_ID and is_new:
                try:
                    from bot.bot import bot
                    notification = (
                        f"🤖 **New Group Added!**\n\n"
                        f"📢 **Group:** {chat_title}\n"
                        f"🆔 **Chat ID:** `{chat_id}`\n"
                        f"👥 **Added by:** {message.from_user.first_name if message.from_user else 'Unknown'}\n"
                        f"📊 **Total Groups:** {len(load_chats())}"
                    )
                    await bot.send_message(Config.LOG_ID, notification)
                except Exception as e:
                    print(f"Failed to send new group notification: {e}")
        else:
            welcome_text = Strings.WELCOME_MSG.format(
                chat=message.chat.title,
                user=member.first_name
            )
            await message.reply_text(welcome_text)

@Client.on_message(filters.video_chat_started)
async def vc_start_handler(client: Client, message: Message):
    try:
        await message.reply_text(Strings.VC_START_MSG)
    except Exception:
        pass

@Client.on_message(filters.video_chat_ended)
async def vc_end_handler(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        # Clear queue and stop streaming if VC ended
        queue_manager.clear_queue(chat_id)
        try:
            await pytgcalls.leave_call(chat_id)
        except:
            pass
        await message.reply_text(Strings.VC_END_MSG)
    except Exception:
        pass
