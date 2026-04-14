# Bot Messages and Templates
from bot.font import Font
import re

class Strings:
    
    @staticmethod
    def _format_emoji_message(emoji_id: str, fallback_emoji: str, text: str) -> str:
        """
        Formats a message with a custom emoji, falling back to a standard Unicode emoji
        if the custom emoji is not supported or causes an error.
        """
        if emoji_id:
            return f"<emoji id=\"{emoji_id}\">{fallback_emoji}</emoji>{' ' if text else ''}{text}"
        return f"{fallback_emoji}{' ' if text else ''}{text}"

    @staticmethod
    def get_message_with_fallback(original_message: str, fallback_emoji_map: dict) -> str:
        """
        Replaces custom emoji tags in a message with their fallback Unicode emojis.
        """
        modified_message = original_message
        for emoji_id, fallback_emoji in fallback_emoji_map.items():
            # Regex to find <emoji id="EMOJI_ID">FALLBACK_EMOJI</emoji>
            # and replace it with just FALLBACK_EMOJI
            modified_message = re.sub(
                rf'<emoji id="{re.escape(emoji_id)}">({re.escape(fallback_emoji)})</emoji>',
                r'\1', # Use the captured fallback emoji
                modified_message
            )
        return modified_message

    # Start Messages
    PRIVATE_START_MSG = (
        "╭───────────────────▣\n"
        "│❍ ʜᴇʏ {user}\n"
        "│❍ ɪ ᴀᴍ {bot_name}\n"
        "├───────────────────▣\n"
        "│❍ ʙᴇsᴛ ǫᴜɪʟɪᴛʏ ғᴇᴀᴛᴜʀᴇs •\n"
        "│❍ ᴍᴀᴅᴇ ʙʏ...{owner_name_mention}\n"
        "╰───────────────────▣"
    )

    ALIVE_MSG = (
        "**{bot_mention} 𝖨𝗌 𝖠𝗅𝗂𝗏𝖾 .**\n\n"
        "✫ **𝖴𝗉𝗍𝗂ᴍᴇ :** {uptime}"
    )

    HELP_MSG = (
        "𝖢𝗁𝗈𝗌𝖾 𝖳𝗁𝖾 𝖢𝖺𝗍𝖾𝗀𝗈𝗋𝗒 𝖥𝗈𝗋 𝖶𝗁𝗂𝼼 𝖸𝗈𝗎 𝖶𝖺𝗇𝗇𝖺 𝖦𝖾𝗍 𝖧𝖾𝗅𝗉 .\n"
        "𝖠𝗌𝗄 𝖸𝗈𝗎𝗋 𝖣𝗈𝗎𝖻𝗍𝗌 𝖠𝗍 {support_mention}\n\n"
        "𝖠𝗅𝗅 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌 𝖢𝖺𝗇 𝖡𝖾 𝖴𝗌𝖾𝖽 𝖶𝗂𝗍𝗁 : /"
    )

    ADMIN_HELP_MSG = (
        "ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs :\n\n"
        "ᴊᴜsᴛ ᴀᴅᴅ ᴄ ɪɴ ᴛʜᴇ sᴛᴀʀᴛɪɴɢ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜsᴇ ᴛʜᴇᴍ ғᴏʀ ᴄʜᴀɴɴᴇʟ.\n\n\n"
        "/pause : ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.\n\n"
        "/resume : ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ.\n\n"
        "/skip : sᴋɪᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ.\n\n"
        "/end ᴏʀ /stop : ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ᴇɴᴅ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.\n\n"
        "/player : ɢᴇᴛ ᴀ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴩʟᴀʏᴇʀ ᴩᴀɴᴇʟ.\n\n"
        "/queue : sʜᴏᴡs ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ʟɪsᴛ."
    )

    AUTH_HELP_MSG = (
        "ᴀᴜᴛʜ ᴜsᴇʀs :\n\n"
        "ᴀᴜᴛʜ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ʙᴏᴛ ᴡɪᴛʜᴏᴜᴛ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ᴄʜᴀᴛ.\n\n"
        "/auth [ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ] : ᴀᴅᴅ ᴀ ᴜsᴇʀ ᴛᴏ ᴀᴜᴛʜ ʟɪsᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ.\n"
        "/unauth [ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ] : ʀᴇᴍᴏᴠᴇ ᴀ ᴀᴜᴛʜ ᴜsᴇʀs ғʀᴏᴍ ᴛʜᴇ ᴀᴜᴛʜ ᴜsᴇʀs ʟɪsᴛ.\n"
        "/authusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴜᴛʜ ᴜsᴇʀs ᴏғ ᴛʜᴇ ɢʀᴏᴜᴩ."
    )

    GCAST_HELP_MSG = (
        "ʙʀᴏᴀᴅᴄᴀsᴛ ғᴇᴀᴛᴜʀᴇ [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs] :\n\n"
        "/broadcast [ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ] : ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.\n\n"
        "ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴏᴅᴇs :\n"
        "-pin : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs.\n"
        "-pinloud : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ sᴇɴᴅ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴛᴏ ᴛʜᴇ ᴍᴇᴍʙᴇʀs.\n"
        "-user : ʙʀᴏᴀᴅᴄᴀsᴛs ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʜᴇ ᴜsᴇʀs ᴡʜᴏ ʜᴀᴠᴇ sᴛᴀʀᴛᴇᴅ ʏᴏᴜʀ ʙᴏᴛ.\n"
        "-assistant : ʙʀᴏᴀᴅᴄᴀsᴛ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ᴀssɪᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ.\n"
        "-nobot : ғᴏʀᴄᴇs ᴛʜᴇ ʙᴏᴛ ᴛᴏ ɴᴏᴛ ʙʀᴏᴀᴅᴄᴀsᴛ ᴛʜᴇ ᴍᴇssᴀɢᴇ..\n\n"
        "ᴇxᴀᴍᴩʟᴇ: /broadcast -user -assistant -pin ᴛᴇsᴛɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ"
    )

    BLCHAT_HELP_MSG = (
        "ᴄʜᴀᴛ ʙʟᴀᴄᴋʟɪsᴛ ғᴇᴀᴛᴜʀᴇ : [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs]\n\n"
        "ʀᴇsᴛʀɪᴄᴛ sʜɪᴛ ᴄʜᴀᴛs ᴛᴏ ᴜsᴇ ᴏᴜʀ ᴘʀᴇᴄɪᴏᴜs ʙᴏᴛ.\n\n"
        "/blacklistchat [ᴄʜᴀᴛ ɪᴅ] : ʙʟᴀᴄᴋʟɪsᴛ ᴀ ᴄʜᴀᴛ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.\n"
        "/whitelistchat [ᴄʜᴀᴛ ɪᴅ] : ᴡʜɪᴛᴇʟɪsᴛ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ.\n"
        "/blacklistedchat : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs."
    )

    BLUSERS_HELP_MSG = (
        "ʙʟᴏᴄᴋ ᴜsᴇʀs: [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs]\n\n"
        "sᴛᴀʀᴛs ɪɢɴᴏʀɪɴɢ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴜsᴇʀ, sᴏ ᴛʜᴀᴛ ʜᴇ ᴄᴀɴ'ᴛ ᴜsᴇ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs.\n\n"
        "/block [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ʙʟᴏᴄᴋ ᴛʜᴇ ᴜsᴇʀ ғʀᴏᴍ ᴏᴜʀ ʙᴏᴛ.\n"
        "/unblock [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ᴜɴʙʟᴏᴄᴋs ᴛʜᴇ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀ.\n"
        "/blockedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs."
    )

    CPLAY_HELP_MSG = (
        "ᴄʜᴀɴɴᴇʟ ᴩʟᴀʏ ᴄᴏᴍᴍᴀɴᴅs:\n\n"
        "ʏᴏᴜ ᴄᴀɴ sᴛʀᴇᴀᴍ ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ ɪɴ ᴄʜᴀɴɴᴇʟ.\n\n"
        "/cplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴀᴜᴅɪᴏ ᴛʀᴀᴄᴋ ᴏɴ ᴄʜᴀɴɴᴇʟ's ᴠɪᴅᴇᴏᴄʜᴀᴛ.\n"
        "/cvplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴠɪᴅᴇᴏ ᴛʀᴀᴄᴋ ᴏɴ ᴄʜᴀɴɴᴇʟ's ᴠɪᴅᴇᴏᴄʜᴀᴛ.\n"
        "/cplayforce or /cvplayforce : sᴛᴏᴩs ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ.\n\n"
        "/channelplay [ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ] ᴏʀ [ᴅɪsᴀʙʟᴇ] : ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀ ɢʀᴏᴜᴩ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʀᴀᴄᴋs ʙʏ ᴛʜᴇ ʜᴇʟᴩ ᴏғ ᴄᴏᴍᴍᴀɴᴅs sᴇɴᴛ ɪɴ ɢʀᴏᴜᴩ."
    )

    GBAN_HELP_MSG = (
        "ɢʟᴏʙᴀʟ ʙᴀɴ ғᴇᴀᴛᴜʀᴇ [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs] :\n\n"
        "/gban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ɢʟᴏʙᴀʟʟʏ ʙᴀɴs ᴛʜᴇ ᴄʜᴜᴛɪʏᴀ ғʀᴏᴍ ᴀʟʟ ᴛʜᴇ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ ʙʟᴀᴄᴋʟɪsᴛ ʜɪᴍ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.\n"
        "/ungban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ɢʟᴏʙᴀʟʟʏ ᴜɴʙᴀɴs ᴛʜᴇ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀ.\n"
        "/gbannedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀs."
    )

    LOOP_HELP_MSG = (
        "ʟᴏᴏᴘ sᴛʀᴇᴀᴍ :\n\n"
        "sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ɪɴ ʟᴏᴏᴘ\n\n"
        "/loop [enable/disable] : ᴇɴᴀʙʟᴇs/ᴅɪsᴀʙʟᴇs ʟᴏᴏᴘ ғᴏʀ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ\n"
        "/loop [1, 2, 3, ...] : ᴇɴᴀʙʟᴇs ᴛʜᴇ ʟᴏᴏᴘ ғᴏʀ ᴛʜᴇ ɢɪᴠᴇɴ ᴠᴀʟᴜᴇ."
    )

    LOG_HELP_MSG = (
        "ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs] :\n\n"
        "/logs : ɢᴇᴛ ʟᴏɢs ᴏғ ᴛʜᴇ ʙᴏᴛ.\n\n"
        "/logger [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] : ʙᴏᴛ ᴡɪʟʟ sᴛᴀʀᴛ ʟᴏɢɢɪɴɢ ᴛʜᴇ ᴀᴄᴛɪᴠɪᴛɪᴇs ʜᴀᴩᴩᴇɴ ᴏɴ ʙᴏᴛ.\n\n"
        "/maintenance [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] : ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ᴛʜᴇ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ ᴏғ ʏᴏᴜʀ ʙᴏᴛ."
    )

    PING_HELP_MSG = (
        "ᴘɪɴɢ & sᴛᴀᴛs :\n\n"
        "/start : sᴛᴀʀᴛs ᴛʜᴇ ᴍᴜsɪᴄ ʙᴏᴛ.\n"
        "/help : ɢᴇᴛ ʜᴇʟᴩ ᴍᴇɴᴜ ᴡɪᴛʜ ᴇxᴩʟᴀɴᴀᴛɪᴏɴ ᴏғ ᴄᴏᴍᴍᴀɴᴅs.\n\n"
        "/ping : sʜᴏᴡs ᴛʜᴇ ᴩɪɴɢ ᴀɴᴅ sʏsᴛᴇᴍ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.\n\n"
        "/stats : sʜᴏᴡs ᴛʜᴇ ᴏᴠᴇʀᴀʟʟ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ."
    )

    PLAY_HELP_MSG = (
        "ᴩʟᴀʏ ᴄᴏᴍᴍᴀɴᴅs :\n\n"
        "v : sᴛᴀɴᴅs ғᴏʀ ᴠɪᴅᴇᴏ ᴩʟᴀʏ.\n"
        "force : sᴛᴀɴᴅs ғᴏʀ ғᴏʀᴄᴇ ᴩʟᴀʏ.\n\n"
        "/play ᴏʀ /vplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.\n\n"
        "/playforce ᴏʀ /vplayforce : sᴛᴏᴩs ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ."
    )

    SHUFFLE_HELP_MSG = (
        "sʜᴜғғʟᴇ ᴏ̨ᴜᴇᴜᴇ :\n\n"
        "/shuffle : sʜᴜғғʟᴇ's ᴛʜᴇ ᴏ̨ᴜᴇᴜᴇ.\n"
        "/queue : sʜᴏᴡs ᴛʜᴇ sʜᴜғғʟᴇᴅ ᴏ̨ᴜᴇᴜᴇ."
    )

    SEEK_HELP_MSG = (
        "sᴇᴇᴋ sᴛʀᴇᴀᴍ :\n\n"
        "/seek [ᴅᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs] : sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴜʀᴀᴛɪᴏɴ.\n"
        "/seekback [ᴅᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs] : ʙᴀᴄᴋᴡᴀʀᴅ sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴜʀᴀᴛɪᴏɴ."
    )

    SONG_HELP_MSG = (
        "sᴏɴɢ ᴅᴏᴡɴʟᴏᴀᴅ\n\n"
        "/song [sᴏɴɢ ɴᴀᴍᴇ/ʏᴛ ᴜʀʟ] : ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴʏ ᴛʀᴀᴄᴋ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ɪɴ ᴍᴘ3 ᴏʀ ᴍᴘ4 ғᴏʀᴍᴀᴛs."
    )

    SPEED_HELP_MSG = (
        "sᴘᴇᴇᴅ ᴄᴏᴍᴍᴀɴᴅs :\n\n"
        "ʏᴏᴜ ᴄᴀɴ ᴄᴏɴᴛʀᴏʟ ᴛʜᴇ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ ᴏғ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ. [ᴀᴅᴍɪɴs ᴏɴʟʏ]\n\n"
        "/speed or /playback : ғᴏʀ ᴀᴅᴊᴜsᴛɪɴɢ ᴛʜᴇ ᴀᴜᴅɪᴏ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ ɪɴ ɢʀᴏᴜᴘ.\n"
        "/cspeed or /cplayback : ғᴏʀ ᴀᴅᴊᴜsᴛɪɴɢ ᴛʜᴇ ᴀᴜᴅɪᴏ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ ɪɴ ᴄʜᴀɴɴᴇʟ."
    )

    # Play Messages
    # Searching Messages
    SEARCHING_MSGS = [
        "💞", "𝚃𝙷𝙸𝚂 𝚂𝙾𝙽𝙶 𝙸𝚂 𝚃𝙾𝚃𝙰𝙻𝙻𝚈 𝙵𝙰𝙱𝚄𝙻𝙰𝚂𝚃𝙸𝙲...🔥🥰", "🔍", "🧪", 
        "ʜᴏʟᴅ ᴏɴ ᴅᴀʀʟɪɴɢ 💗", "⚡️", "🔥", "ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...❤‍🔥", "🎩", "🌈", 
        "🍷", "🥂", "🥃", "ᴀᴄᴄʜɪ ᴘᴀsᴀɴᴅ ʜᴀɪ 🥰", 
        "ʟᴏᴏᴋɪɴɢ ғᴏʀ ʏᴏᴜʀ sᴏɴɢ... ᴡᴀɪᴛ! 💗", "🪄", "💌", 
        "ᴏᴋ ʙᴀʙʏ ᴡᴀɪᴛ😘 ғᴇᴡ sᴇᴄᴏɴᴅs", "ᴀʜʜ! ɢᴏᴏᴅ ᴄʜᴏɪᴄᴇ ʜᴏʟᴅ ᴏɴ...", 
        "ᴡᴏᴡ! ɪᴛ's ᴍʏ ғᴀᴠᴏʀɪᴛᴇ sᴏɴɢ...", "ɴɪᴄᴇ ᴄʜᴏɪᴄᴇ..! ᴡᴀɪᴛ 𝟸 sᴇᴄᴏɴᴅ", 
        "🔎", "🍹", "🍻", "ɪ ʟᴏᴠᴇ ᴛʜᴀᴛ sᴏɴɢ..!😍", "💥", "💗", "✨"
    ]

    @classmethod
    def get_searching_msg(cls, query):
        import random
        return random.choice(cls.SEARCHING_MSGS)

    DOWNLOADING_TG_MSG = "📥 " + Font.small_caps("Downloading Telegram file... Please wait.")
    
    @classmethod
    def get_playing_msg(cls):
        from config import Config
        return cls._format_emoji_message(Config.PLAYING_EMOJI_ID, "🎵", "")

    @classmethod
    def get_streaming_started_msg(cls, title, duration, artist, url=None, is_video=False):
        from config import Config
        # Shorten title to 25 characters
        short_title = (title[:25] + '...') if len(title) > 25 else title
        title_mention = f"[{short_title}]({url})" if url else short_title
        header = "❖  𝛅ᴛᴧʀᴛєᴅ  " + ("ᴠɪᴅєᴏ" if is_video else "ᴧᴜᴅɪᴏ") + "  𝛅ᴛʀєᴧϻɪηɢ"
        return (
            f"<blockquote>"
            f"{header}\n"
            f"❍ ᴛɪᴛʟє : {title_mention}\n"
            f"❍ ᴅᴜʀᴧᴛɪση : {duration} ϻɪηᴜᴛєs\n"
            f"❍ ʙʏ : {artist}"
            f"</blockquote>"
        )
        
    @classmethod
    def get_added_queue_msg(cls, title, pos, user, duration="N/A", url=None):
        from config import Config
        # Shorten title to 25 characters
        short_title = (title[:25] + '...') if len(title) > 25 else title
        title_mention = f"[{short_title}]({url})" if url else short_title
        header = f"❖ ᴧᴅᴅєᴅ ᴛᴏ ǫᴜєᴜє ᴧᴛ #{pos}"
        return (
            f"▎ {header}\n"
            f"▎ ❍ ᴛɪᴛʟє : {title_mention}\n"
            f"▎ ❍ ᴅᴜʀᴧᴛɪση : {duration}\n"
            f"▎ ❍ ʙʏ : {user}"
        )
    
    # Queue Messages
    @classmethod
    def get_queue_header(cls, chat):
        from config import Config
        return cls._format_emoji_message(Config.QUEUE_EMOJI_ID, "📋", Font.small_caps("Current Playback Queue for {chat}:").format(chat=chat)) + "\n\n"

    QUEUE_EMPTY = "❌ " + Font.small_caps("The queue is currently empty.")

    @classmethod
    def get_queue_now_playing(cls, title):
        from config import Config
        playing_emoji = cls._format_emoji_message(Config.PLAYING_EMOJI_ID, "🎵", Font.small_caps("Now Playing:"))
        return f"<blockquote>{playing_emoji} `{title}`</blockquote>\n"

    QUEUE_ITEM = "{pos}. `{title}` (" + Font.math("Added by {user}") + ")\n"
    
    # Skip Messages
    @classmethod
    def get_skipped_msg(cls, title):
        from config import Config
        skip_emoji = cls._format_emoji_message(Config.SKIP_EMOJI_ID, "⏭", Font.small_caps("Skipped!"))
        playing_emoji = cls._format_emoji_message(Config.PLAYING_EMOJI_ID, "🎵", Font.small_caps("Now Playing:"))
        return (
            f"<blockquote>"
            f"{skip_emoji}\n\n"
            f"{playing_emoji} `{title}`"
            f"</blockquote>"
        )

    SKIP_EMPTY_MSG = "❌ " + Font.small_caps("The queue is empty.")
    SKIP_NO_MORE_MSG = "⏭ " + Font.small_caps("Skipped!") + " ɴᴏ ᴍᴏʀᴇ ᴛʀᴀᴄᴋs ɪɴ ᴛʜᴇ ǫᴜᴇᴜᴇ."
    
    # Stop Messages
    @classmethod
    def get_stop_msg(cls):
        from config import Config
        return cls._format_emoji_message(Config.STOP_EMOJI_ID, "⏹", Font.small_caps("Playback stopped and queue cleared successfully."))
    
    # Ping Messages
    PING_MSG = "🏓 " + Font.small_caps("Pinging...")

    @classmethod
    def get_pong_msg(cls, ms):
        from config import Config
        return cls._format_emoji_message(Config.PING_EMOJI_ID, "🏓", Font.small_caps("Pong!")) + f"\n\n⚡ " + Font.small_caps("Response Time:") + f" `{ms}ms`"
    
    # Welcome Message
    WELCOME_MSG = (
        "✨ " + Font.small_caps("Welcome to {chat}, {user}!") + "\n\n"
        "ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ʜɪɢʜ-ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ ɪɴ ᴏᴜʀ ᴠɪsɪᴄᴇ ᴄʜᴀᴛ. "
        "ᴛʏᴘᴇ `/play <song>` ᴛᴏ ɢᴇᴛ sᴛᴀʀᴛᴇᴅ!"
    )
    
    # Service Messages
    @classmethod
    def get_welcome_msg(cls, user_mention, chat_title):
        return (
            f"✨ **Welcome to {chat_title}, {user_mention}!** ✨\n\n"
            "ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ʜɪɢʜ-ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ ɪɴ ᴏᴜʀ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ. "
            "ᴛʏᴘᴇ `/play <song>` ᴛᴏ ɢᴇᴛ sᴛᴀʀᴛᴇᴅ!"
        )

    VC_START_MSG = (
        "🔊 **ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ !**\n\n"
        "ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʜᴀs ʙᴇᴇɴ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ. "
        "ʏᴏᴜ ᴄᴀɴ ɴᴏᴡ sᴛʀᴇᴀᴍ ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ."
    )

    VC_END_MSG = (
        "🔇 **ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ !**\n\n"
        "ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʜᴀs ʙᴇᴇɴ ᴇɴᴅᴇᴅ. "
        "sᴛʀᴇᴀᴍɪɴɢ sᴛᴏᴘᴘᴇᴅ ᴀɴᴅ ǫᴜᴇᴜᴇ ᴄʟᴇᴀʀᴇᴅ."
    )

    # Errors
    @classmethod
    def get_error_msg(cls, error):
        from config import Config
        return cls._format_emoji_message(Config.ERROR_EMOJI_ID, "❌", Font.small_caps("Error:")) + f" `{error}`"

    PLAY_PROMPT_MSG = "❗ " + Font.small_caps("Please provide a song name, link, or reply to an audio file.")

    # Play Error Message
    PLAY_ERROR_MSG = (
        "ʀᴜᴋ ɴ ʙᴀᴊᴀᴛɪ ʜᴏᴜɴ\n"
        "ᴛʜɪs ᴛʀᴀᴄᴋ ᴄᴏᴜʟᴅɴ'ᴛ ʙᴇ ᴘʟᴀʏᴇᴅ.\n"
        "ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ sᴏɴɢ. 🥀"
    )

    # Settings Messages
    SETTINGS_TITLE = "⚙️ 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀 𝗣𝗮𝗻𝗲𝗹"
    SETTINGS_DESC = (
        "╭───────────────────▣\n"
        "│ ◈ ᴄᴜsᴛᴏᴍɪᴢᴇ ʏᴏᴜʀ ʙᴏᴛ sᴇᴛᴛɪɴɢs\n"
        "│ ◈ ᴛᴀᴘ ᴀ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴛᴏɢɢʟᴇ\n"
        "╰───────────────────▣"
    )
    
    PLAY_MODE_CHANGED = "✅ ᴘʟᴀʏ ᴍᴏᴅᴇ ᴄʜᴀɴɢᴇᴅ ᴛᴏ: {}"
    LANGUAGE_CHANGED = "✅ ʟᴀɴɢᴜᴀɢᴇ ᴄʜᴀɴɢᴇᴅ ᴛᴏ: {}"
    SKIP_PERM_CHANGED = "✅ sᴋɪᴘ ᴘᴇʀᴍɪssɪᴏɴ ᴄʜᴀɴɢᴇᴅ ᴛᴏ: {}"
    AUTH_USERS_TITLE = "👥 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗨𝘀𝗲𝗿𝘀"
    AUTH_USERS_EMPTY = "ɴᴏ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs ғᴏᴜɴᴅ.\n\nᴜsᴇ `/auth` ᴛᴏ ᴀᴅᴅ ᴜsᴇʀs."

