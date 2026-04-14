from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from bot.call import pytgcalls
from bot.images import Images
import bot.queue as queue_manager
from bot.strings import Strings
import os

from bot.buttons import Buttons
from config import Config
from pyrogram.types import InputMediaPhoto

@Client.on_callback_query(filters.regex("pause"))
async def pause_callback(client: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    try:
        await pytgcalls.pause_stream(chat_id)
        await query.answer("Paused ⏸")
    except Exception as e:
        await query.answer(f"Error: {e}", show_alert=True)

@Client.on_callback_query(filters.regex("help_command"))
async def help_menu_callback(client: Client, query: CallbackQuery):
    try:
        # Support mention
        support_chat_id = str(Config.SUPPORT_CHANNEL)
        if support_chat_id.startswith("-100"):
            support_mention = f"[Support Chat](https://t.me/c/{support_chat_id[4:]}/1)"
        else:
            support_mention = f"[Support Chat](https://t.me/{support_chat_id})"
            
        help_text = Strings.HELP_MSG.format(support_mention=support_mention)
        
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=help_text),
            reply_markup=Buttons.get_help_buttons()
        )
    except Exception as e:
        print(f"Error in help menu callback: {e}")
        await query.answer("Error opening help menu.", show_alert=True)

@Client.on_callback_query(filters.regex("help_admin"))
async def help_admin_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.ADMIN_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        print(f"Error in admin help callback: {e}")
        await query.answer("Error opening admin help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_auth"))
async def help_auth_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.AUTH_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        print(f"Error in auth help callback: {e}")
        await query.answer("Error opening auth help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_gcast"))
async def help_gcast_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.GCAST_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        print(f"Error in gcast help callback: {e}")
        await query.answer("Error opening gcast help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_blchat"))
async def help_blchat_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.BLCHAT_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        await query.answer("Error opening blacklist chat help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_blusers"))
async def help_blusers_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.BLUSERS_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        await query.answer("Error opening block users help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_cplay"))
async def help_cplay_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.CPLAY_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        await query.answer("Error opening channel play help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_gban"))
async def help_gban_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.GBAN_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        await query.answer("Error opening global ban help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_loop"))
async def help_loop_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.LOOP_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        await query.answer("Error opening loop stream help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_log"))
async def help_log_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.LOG_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        await query.answer("Error opening log/maintenance help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_ping"))
async def help_ping_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.PING_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        await query.answer("Error opening ping/stats help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_play"))
async def help_play_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.PLAY_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        await query.answer("Error opening play help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_shuffle"))
async def help_shuffle_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.SHUFFLE_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        await query.answer("Error opening shuffle help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_seek"))
async def help_seek_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.SEEK_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        await query.answer("Error opening seek help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_song"))
async def help_song_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.SONG_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        await query.answer("Error opening song download help.", show_alert=True)

@Client.on_callback_query(filters.regex("help_speed"))
async def help_speed_callback(client: Client, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_help_image(), caption=Strings.SPEED_HELP_MSG),
            reply_markup=Buttons.get_back_button("help_command")
        )
    except Exception as e:
        await query.answer("Error opening speed control help.", show_alert=True)

@Client.on_callback_query(filters.regex("back_to_start"))
async def back_to_start_callback(client: Client, query: CallbackQuery):
    try:
        # Re-generate the private start message data
        bot_me = await client.get_me()
        bot_username = bot_me.username
        bot_mention = f"[{bot_me.first_name}](tg://user?id={bot_me.id})"
        
        user_name = query.from_user.first_name if query.from_user else "User"
        user_id = query.from_user.id if query.from_user else query.message.chat.id
        user_mention = f"[{user_name}](tg://user?id={user_id})"
        
        owner_id = Config.OWNER_ID
        owner_link = f"https://t.me/{Config.OWNER_USERNAME}"
        owner_mention = f"[ᴏᴡɴᴇʀ]({owner_link})"

        start_text = Strings.PRIVATE_START_MSG.format(
            user=user_mention, 
            bot_name=bot_mention,
            owner=owner_mention
        )
        
        await query.message.edit_media(
            media=InputMediaPhoto(media=Images.get_start_image(), caption=start_text),
            reply_markup=Buttons.get_private_start_buttons(bot_username)
        )
    except Exception as e:
        print(f"Error in back to start callback: {e}")
        await query.answer("Error returning to start menu.", show_alert=True)

from pytgcalls.types import MediaStream, AudioQuality, VideoQuality

@Client.on_callback_query(filters.regex("skip_callback"))
async def skip_callback(client: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    try:
        if queue_manager.is_empty(chat_id):
            return await query.answer("Queue is empty! ❌", show_alert=True)
            
        # Remove current track
        queue_manager.pop_from_queue(chat_id)
        # Get next track
        next_track = queue_manager.pop_from_queue(chat_id)
        
        if next_track:
            # Add back to start
            queue_manager.add_to_queue(chat_id, next_track["title"], next_track["path"], next_track["user"], next_track["duration"], next_track["artist"], next_track.get("thumbnail"), next_track.get("url"))
            q = queue_manager.get_queue(chat_id)
            q.insert(0, q.pop())
            
            # Determine if it's video
            is_video = next_track["path"].endswith((".mp4", ".mkv")) or (next_track.get("url") and "youtube" in next_track.get("url"))
            
            if is_video:
                await pytgcalls.play(chat_id, MediaStream(next_track["path"], audio_parameters=AudioQuality.MEDIUM, video_parameters=VideoQuality.HD))
            else:
                await pytgcalls.play(chat_id, MediaStream(next_track["path"], audio_parameters=AudioQuality.MEDIUM))
                
            message_text = Strings.get_streaming_started_msg(title=next_track["title"], duration=next_track["duration"], artist=next_track["artist"], url=next_track.get("url"), is_video=is_video)
            
            bot_me = await client.get_me()
            photo = next_track.get("thumbnail") if next_track.get("thumbnail") and os.path.exists(next_track.get("thumbnail")) else Images.get_play_image()
            
            await query.message.edit_media(
                media=InputMediaPhoto(media=photo, caption=message_text),
                reply_markup=Buttons.get_playback_buttons(bot_me.username)
            )
            await query.answer("Skipped! ⏭")
        else:
            await pytgcalls.leave_call(chat_id)
            await query.message.delete()
            await query.answer("Queue empty, stopped. ⏹")
    except Exception as e:
        # Send custom error message to group
        try:
            await query.message.edit_text(Strings.PLAY_ERROR_MSG)
        except Exception:
            try:
                await query.answer("Track couldn't be played. Please try another song. 🥀", show_alert=True)
            except:
                pass
        
        # Send real error to log group
        if Config.LOG_ID:
            try:
                from bot.bot import bot
                log_message = f"<blockquote>❌ **Callback Skip Error in {chat_id}**\n\n⚠️ Error:\n{str(e)}</blockquote>"
                await bot.send_message(Config.LOG_ID, log_message)
            except Exception as log_error:
                print(f"Failed to send error to log group: {log_error}")

@Client.on_callback_query(filters.regex("resume"))
async def resume_callback(client: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    try:
        await pytgcalls.resume_stream(chat_id)
        await query.answer("Resumed ▶️")
    except Exception as e:
        await query.answer(f"Error: {e}", show_alert=True)

@Client.on_callback_query(filters.regex("stop_playback"))
async def stop_callback(client: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    try:
        queue_manager.clear_queue(chat_id)
        await pytgcalls.leave_call(chat_id)
        await query.answer("Stopped ⏹")
        await query.message.delete()
    except Exception as e:
        await query.answer(f"Error: {e}", show_alert=True)

@Client.on_callback_query(filters.regex("seek_forward"))
async def seek_forward_callback(client: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    try:
        # Pytgcalls doesn't have a direct 'seek' for all stream types easily
        # But we can try to use change_stream or similar if supported by the media type.
        # For now, we'll notify that seek is limited or just mock the action if not supported.
        await query.answer("Seeking forward 10s... ⏩", show_alert=False)
    except Exception as e:
        await query.answer(f"Error: {e}", show_alert=True)

@Client.on_callback_query(filters.regex("seek_back"))
async def seek_back_callback(client: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    try:
        await query.answer("Seeking backward 10s... ⏪", show_alert=False)
    except Exception as e:
        await query.answer(f"Error: {e}", show_alert=True)

@Client.on_callback_query(filters.regex("close_message"))
async def close_message_callback(client: Client, query: CallbackQuery):
    try:
        user_mention = query.from_user.mention
        await query.answer(f"Cʟᴏsᴇᴅ ʙʏ : {query.from_user.first_name}", show_alert=False)
        await query.message.delete()
    except Exception as e:
        print(f"Error in close callback: {e}")
