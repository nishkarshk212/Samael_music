from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config

class Buttons:
    @staticmethod
    def get_private_start_buttons(bot_username: str):
        """
        Returns the inline keyboard for the private start message.
        """
        # Bot invite link
        invite_link = f"https://t.me/{bot_username}?startgroup=true"
        
        # Format channel links (handle both IDs and usernames)
        def format_link(chat_id):
            chat_id = str(chat_id)
            if chat_id.startswith("-100"):
                return f"https://t.me/c/{chat_id[4:]}/1"
            return f"https://t.me/{chat_id}"

        # Support and Updates buttons
        support_link = format_link(Config.SUPPORT_CHANNEL)
        updates_link = format_link(Config.UPDATES_CHANNEL)

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="✨ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ✨",
                        url=invite_link
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="ꜱᴜᴘᴘᴏʀᴛ",
                        url=support_link
                    ),
                    InlineKeyboardButton(
                        text="ᴜᴘᴅᴀᴛᴇꜱ",
                        url=updates_link
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅ",
                        callback_data="help_command"
                    )
                ]
            ]
        )
        return keyboard

    @staticmethod
    def get_help_buttons():
        """
        Returns the inline keyboard for the help menu.
        """
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("• ᴧᴅᴍɪɴ •", callback_data="help_admin"),
                    InlineKeyboardButton("• ᴧᴜᴛʜ •", callback_data="help_auth"),
                    InlineKeyboardButton("• ɢ-ᴄᴧsᴛ •", callback_data="help_gcast")
                ],
                [
                    InlineKeyboardButton("• ʙʟ-ᴄʜᴧᴛ •", callback_data="help_blchat"),
                    InlineKeyboardButton("• ʙʟ-ᴜsᴇʀs •", callback_data="help_blusers"),
                    InlineKeyboardButton("• ᴄ-ᴘʟᴧʏ •", callback_data="help_cplay")
                ],
                [
                    InlineKeyboardButton("• ɢ-ʙᴧɴ •", callback_data="help_gban"),
                    InlineKeyboardButton("• ʟᴏᴏᴘ •", callback_data="help_loop"),
                    InlineKeyboardButton("• ʟᴏɢ •", callback_data="help_log")
                ],
                [
                    InlineKeyboardButton("• ᴘɪɴɢ •", callback_data="help_ping"),
                    InlineKeyboardButton("• ᴘʟᴧʏ •", callback_data="help_play"),
                    InlineKeyboardButton("• sʜᴜғғʟᴇ •", callback_data="help_shuffle")
                ],
                [
                    InlineKeyboardButton("• sᴇᴇᴋ •", callback_data="help_seek"),
                    InlineKeyboardButton("• sᴏɴɢ •", callback_data="help_song"),
                    InlineKeyboardButton("• sᴘᴇᴇᴅ •", callback_data="help_speed")
                ],
                [
                    InlineKeyboardButton("= ʙᴧᴄᴋ =", callback_data="back_to_start")
                ]
            ]
        )
        return keyboard

    @staticmethod
    def get_back_button(callback_data: str):
        """
        Returns a single back button.
        """
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="= ʙᴧᴄᴋ =",
                        callback_data=callback_data
                    )
                ]
            ]
        )
        return keyboard

    @staticmethod
    def get_settings_buttons(play_mode="Audio", language="English", skip_perm="Admin Only"):
        """
        Returns the inline keyboard for the settings panel.
        """
        # Play mode button with toggle
        play_mode_icon = "🎵" if play_mode == "Audio" else "🎬"
        play_mode_text = f"{play_mode_icon} {play_mode}"
        
        # Language button with toggle
        lang_icon = "🌐"
        language_text = f"{lang_icon} {language}"
        
        # Skip permission button
        skip_icon = "👑" if skip_perm == "Admin Only" else "👥"
        skip_text = f"{skip_icon} {skip_perm}"
        
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=play_mode_text,
                        callback_data="toggle_play_mode"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=language_text,
                        callback_data="toggle_language"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=skip_text,
                        callback_data="toggle_skip_perm"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="👥 Auth Users",
                        callback_data="settings_auth_users"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="✖️ Close",
                        callback_data="close_message"
                    )
                ]
            ]
        )
        return keyboard

    @staticmethod
    def get_close_button():
        """
        Returns a single close button.
        """
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="ᴄʟᴏꜱᴇ",
                        callback_data="close_message"
                    )
                ]
            ]
        )
        return keyboard

    @staticmethod
    def get_group_start_buttons(bot_username: str):
        """
        Returns the inline keyboard for the group start/alive message.
        """
        # Bot invite link
        invite_link = f"https://t.me/{bot_username}?startgroup=true"
        
        # Support link
        support_chat_id = str(Config.SUPPORT_CHANNEL)
        if support_chat_id.startswith("-100"):
            support_link = f"https://t.me/c/{support_chat_id[4:]}/1"
        else:
            support_link = f"https://t.me/{support_chat_id}"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="✨ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ✨",
                        url=invite_link
                    ),
                    InlineKeyboardButton(
                        text="ꜱᴜᴘᴘᴏʀᴛ",
                        url=support_link
                    )
                ]
            ]
        )
        return keyboard

    @staticmethod
    def get_playback_buttons(bot_username: str):
        """
        Returns the inline keyboard for playback messages.
        """
        # Bot invite link
        invite_link = f"https://t.me/{bot_username}?startgroup=true"
        
        # Support link
        support_chat_id = str(Config.SUPPORT_CHANNEL)
        if support_chat_id.startswith("-100"):
            support_link = f"https://t.me/c/{support_chat_id[4:]}/1"
        else:
            support_link = f"https://t.me/{support_chat_id}"

        # Owner link
        owner_link = f"https://t.me/{Config.OWNER_USERNAME}"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="⏸", callback_data="pause"),
                    InlineKeyboardButton(text="▶️", callback_data="resume"),
                    InlineKeyboardButton(text="⏭", callback_data="skip_callback"),
                    InlineKeyboardButton(text="⏹", callback_data="stop_playback")
                ],
                [
                    InlineKeyboardButton(text="⏪ 10s", callback_data="seek_back"),
                    InlineKeyboardButton(text="⏩ 10s", callback_data="seek_forward")
                ],
                [
                    InlineKeyboardButton(
                        text="✨ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ✨",
                        url=invite_link
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="ꜱᴜᴘᴘᴏʀᴛ",
                        url=support_link
                    ),
                    InlineKeyboardButton(
                        text="ᴏᴡɴᴇʀ",
                        url=owner_link
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="ᴄʟᴏꜱᴇ",
                        callback_data="close_message"
                    )
                ]
            ]
        )
        return keyboard
