from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import GetCustomEmojiDocuments, GetStickerSet
from pyrogram.raw.types import DocumentAttributeCustomEmoji
from config import Config
import random

@Client.on_message(filters.command("setpack") & filters.user(Config.SUDO_USERS))
async def set_pack_cmd(client: Client, message: Message):
    """Extract all emojis from a premium emoji's pack and distribute them across bot messages."""
    emoji_to_extract = None
    
    if message.reply_to_message and message.reply_to_message.entities:
        for entity in message.reply_to_message.entities:
            custom_emoji_id = getattr(entity, "custom_emoji_id", None)
            if custom_emoji_id:
                emoji_to_extract = custom_emoji_id
                break
    elif message.entities:
        for entity in message.entities:
            custom_emoji_id = getattr(entity, "custom_emoji_id", None)
            if custom_emoji_id:
                emoji_to_extract = custom_emoji_id
                break
                
    if not emoji_to_extract:
        return await message.reply_text("❌ Please reply to a premium emoji or send one with the command to extract the pack.")

    m = await message.reply_text("🔍 Extracting emoji pack details...")
    
    try:
        # Get the custom emoji documents using raw API
        custom_emojis = await client.invoke(GetCustomEmojiDocuments(document_id=[int(emoji_to_extract)]))
        if not custom_emojis:
            return await m.edit("❌ Could not find details for this premium emoji.")
            
        # Extract the sticker set information from the document attributes
        sticker_set_input = None
        for attribute in custom_emojis[0].attributes:
            if isinstance(attribute, DocumentAttributeCustomEmoji):
                sticker_set_input = attribute.stickerset
                break
                
        if not sticker_set_input:
             return await m.edit("❌ This emoji doesn't seem to belong to a named pack.")

        # Get the full sticker set (which contains all emojis in the pack)
        sticker_set = await client.invoke(GetStickerSet(stickerset=sticker_set_input, hash=0))
        emoji_ids = []
        for sticker_doc in sticker_set.documents:
            for attribute in sticker_doc.attributes:
                if isinstance(attribute, DocumentAttributeCustomEmoji):
                    emoji_ids.append(str(attribute.custom_emoji_id))
                    break

        if not emoji_ids:
            return await m.edit("❌ No custom emoji IDs found in this pack.")

        # Store the pack IDs
        Config.EMOJI_PACK_IDS = emoji_ids
        
        # Distribute them!
        count = len(emoji_ids)
        Config.PLAYING_EMOJI_ID = emoji_ids[0]
        Config.SEARCH_EMOJI_ID = emoji_ids[min(1, count-1)]
        Config.PING_EMOJI_ID = emoji_ids[min(2, count-1)]
        Config.STOP_EMOJI_ID = emoji_ids[min(3, count-1)]
        Config.QUEUE_EMOJI_ID = emoji_ids[min(4, count-1)]
        Config.SKIP_EMOJI_ID = emoji_ids[min(5, count-1)]
        Config.ERROR_EMOJI_ID = emoji_ids[min(6, count-1)]
        Config.SUCCESS_EMOJI_ID = emoji_ids[min(7, count-1)]
        
        await m.edit(
            f"✅ **Emoji Pack Extracted!**\n\n"
            f"📦 **Pack:** `{getattr(sticker_set.set, 'title', 'Premium Pack')}`\n"
            f"🔢 **Total Emojis:** `{count}`\n\n"
            f"The bot is now using different premium emojis from this pack for all messages (Playing, Searching, Queue, etc.)!"
        )
        
    except Exception as e:
        await m.edit(f"❌ Error extracting pack: `{str(e)}`")


@Client.on_message(filters.command("setemoji") & filters.user(Config.SUDO_USERS))
async def set_emoji_cmd(client: Client, message: Message):
    """Set the playing emoji manually by ID or by replying to a premium emoji."""
    emoji_id_to_set = None

    if message.reply_to_message and message.reply_to_message.entities:
        for entity in message.reply_to_message.entities:
            custom_emoji_id = getattr(entity, "custom_emoji_id", None)
            if custom_emoji_id:
                emoji_id_to_set = str(custom_emoji_id)
                break
    elif message.entities:
        for entity in message.entities:
            custom_emoji_id = getattr(entity, "custom_emoji_id", None)
            if custom_emoji_id:
                emoji_id_to_set = str(custom_emoji_id)
                break
    
    if len(message.command) > 1:
        emoji_id_to_set = message.command[1]
    
    if not emoji_id_to_set:
        await message.reply_text("❌ Reply to a premium emoji, send one with the command, or provide the ID to set it.")
        return

    Config.PLAYING_EMOJI_ID = emoji_id_to_set
    await message.reply_text(f"✅ Playing emoji updated to ID: `{emoji_id_to_set}`")


@Client.on_message(filters.user(Config.SUDO_USERS) & filters.private & ~filters.command(["setemoji", "setpack"]))
async def extract_emoji_private(client: Client, message: Message):
    """Automatically extract and set the emoji if a sudo user sends a premium emoji in private chat."""
    if message.entities:
        for entity in message.entities:
            custom_emoji_id = getattr(entity, "custom_emoji_id", None)
            if custom_emoji_id:
                # If it's a single emoji in private, we'll ask if they want to set the pack
                Config.PLAYING_EMOJI_ID = str(custom_emoji_id)
                await message.reply_text(
                    f"✅ Extracted Premium Emoji ID: `{custom_emoji_id}`\n\n"
                    "I've set this as the 'Now Playing' emoji.\n\n"
                    "💡 **Tip:** Use `/setpack` by replying to this emoji to use the entire pack for all bot messages!"
                )
                return
