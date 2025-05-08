from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from utils import is_admin, humanbytes
import config
import logging

logger = logging.getLogger(__name__)
db = Database()

@Client.on_message(filters.command("stats"))
async def stats_command(client: Client, message: Message):
    if not is_admin(message):
        await message.reply_text("⚠️ You are not authorized to use this command!")
        return

    try:
        stats = await db.get_stats()

        stats_text = "**📊 Bot Statistics**\n\n"
        stats_text += f"📁 **Files:** `{stats.get('total_files', 0)}`\n"
        stats_text += f"👥 **Users:** `{stats.get('total_users', 0)}`\n"
        stats_text += f"📥 **Downloads:** `{stats.get('total_downloads', 0)}`\n"

        if stats.get('total_size'):
            stats_text += f"💾 **Size:** `{humanbytes(stats['total_size'])}`\n"

        if 'active_autodelete_files' in stats:
            stats_text += f"🕒 **Auto-Delete Files:** `{stats['active_autodelete_files']}`\n"

        if getattr(config, 'DEFAULT_AUTO_DELETE', None):
            stats_text += f"\n⏱ **Auto-Delete Time:** `{config.DEFAULT_AUTO_DELETE}` minutes"

        await message.reply_text(stats_text)

    except Exception as e:
        logger.error(f"Stats command error: {e}")
        await message.reply_text("❌ Error fetching statistics. Please try again later.")
