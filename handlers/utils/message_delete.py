from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio, logging

logger = logging.getLogger(__name__)

async def schedule_message_deletion(client: Client, chat_id: int, msg_ids: list, mins: int, link: str = None):
    await asyncio.sleep(mins * 60)
    try:
        await client.delete_messages(chat_id, msg_ids)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Get Again", url=link)]]) if link else None
        await client.send_message(
            chat_id,
            "<codeblock>This file was auto-deleted after the set time to save space.\nUse the button below to get it again.</codeblock>",
            reply_markup=kb,
            parse_mode="markdown"
        )
    except Exception as e:
        logger.error(f"Error in deletion: {e}")
