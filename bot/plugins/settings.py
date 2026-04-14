from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.strings import Strings
from bot.buttons import Buttons
from bot.images import Images
from config import Config
from pyrogram.types import InputMediaPhoto

# In-memory storage for group settings (can be moved to database later)
group_settings = {}

def get_group_settings(chat_id):
    """Get settings for a group, or return defaults"""
    if chat_id not in group_settings:
        group_settings[chat_id] = {
            "play_mode": "Audio",  # Audio or Video
            "language": "English",  # English, Hindi, etc.
            "skip_permission": "Admin Only",  # Admin Only or Everyone
            "auth_users": []  # List of user IDs
        }
    return group_settings[chat_id]

@Client.on_message(filters.command("settings") & filters.group)
async def settings_command(client: Client, message: Message):
    """Open settings panel for the group"""
    chat_id = message.chat.id
    
    # Check if user is admin
    user_id = message.from_user.id
    chat_member = await client.get_chat_member(chat_id, user_id)
    
    if chat_member.status not in ["creator", "administrator"]:
        return await message.reply_text("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴀᴄᴄᴇss sᴇᴛᴛɪɴɢs.")
    
    settings = get_group_settings(chat_id)
    
    settings_text = Strings.SETTINGS_TITLE + "\n\n" + Strings.SETTINGS_DESC
    
    try:
        await message.reply_photo(
            photo=Images.get_play_image(),
            caption=settings_text,
            reply_markup=Buttons.get_settings_buttons(
                play_mode=settings["play_mode"],
                language=settings["language"],
                skip_perm=settings["skip_permission"]
            )
        )
    except Exception:
        await message.reply_text(
            settings_text,
            reply_markup=Buttons.get_settings_buttons(
                play_mode=settings["play_mode"],
                language=settings["language"],
                skip_perm=settings["skip_permission"]
            )
        )
