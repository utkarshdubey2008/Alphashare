# -- coding: utf-8 --

import asyncio
import logging
from pyrogram import Client, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

logger = logging.getLogger(__name__)

async def schedule_message_deletion(client: Client, chat_id: int, msg_ids: list, mins: int, link: str = None):
    await asyncio.sleep(mins * 60)
    try:
        await client.delete_messages(chat_id, msg_ids)

        kb = None
        if link:
            
            start_link = f"https://t.me/{config.BOT_NAME}?start={link}"
            kb = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔄 Get Again", url=start_link)]]
            )

        await client.send_message(
            chat_id,
            "<blockquote>🗑️ This file was auto-deleted after the set time to save space.\n"
            "Use the button below to get it again.</blockquote>",
            reply_markup=kb,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Error in deletion: {e}")
