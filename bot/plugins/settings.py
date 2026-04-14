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
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        print(f"Settings command by {message.from_user.first_name} ({user_id}) in chat {chat_id}")
        
        # Check if user is admin or creator
        try:
            chat_member = await client.get_chat_member(chat_id, user_id)
            print(f"User status: {chat_member.status}")
            
            # Fix: Check enum values properly
            if chat_member.status.value not in ["creator", "administrator"]:
                print(f"User {user_id} is not admin (status: {chat_member.status.value})")
                return await message.reply_text("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴀᴄᴄᴇss sᴇᴛᴛɪɴɢs.")
            else:
                print(f"User {user_id} is admin/creator - allowing access")
        except Exception as e:
            print(f"Error checking admin status: {e}")
            # If we can't check, allow the command (fallback)
            print("Allowing command due to admin check error")
        
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
            print(f"Settings panel sent to chat {chat_id}")
        except Exception as e:
            print(f"Error sending settings photo: {e}")
            await message.reply_text(
                settings_text,
                reply_markup=Buttons.get_settings_buttons(
                    play_mode=settings["play_mode"],
                    language=settings["language"],
                    skip_perm=settings["skip_permission"]
                )
            )
    except Exception as e:
        print(f"Critical error in settings command: {e}")
        import traceback
        traceback.print_exc()
        await message.reply_text("❌ Error occurred while opening settings.")
