from database import Database
from pyrogram import Client, filters
from pyrogram.types import Message
from config  import OWNER_ID

import logging

db = Database()

logger = logging.getLogger(__name__)



async def add_admin_to_db(user_id: int) -> bool:
    try:
        existing = await db.admin_collection.find_one({"user_id": user_id})
        if existing:
            return False

        await db.admin_collection.insert_one({"user_id": user_id})
        return True

    except Exception as e:
        logger.error(f"Error adding admin: {str(e)}")
        return False


async def remove_admin_from_db(user_id: int) -> bool:
    try:
        result = await db.admin_collection.delete_one({"user_id": user_id})
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Error removing admin: {str(e)}")
        return False
    
async def get_all_admin_ids() -> list:
    try:
        cursor = db.admin_collection.find({})
        admins = await cursor.to_list(length=None)
        admin_ids = [admin['user_id'] for admin in admins]

        admin_ids.append(OWNER_ID)
        return list(set(admin_ids))

    except Exception as e:
        logger.error(f"Error fetching admin list: {str(e)}")
        return [OWNER_ID]




@Client.on_message(filters.command("addadmin") & filters.private)
async def add_admin_cmd(client: Client, message: Message):
    from_user_id = message.from_user.id

    if from_user_id != OWNER_ID:
        await message.reply_text("__Only the owner can add new admins!__")
        return
    
    if len(message.command) != 2:
        return await message.reply_text("**Usage:** `/addadmin user_id`")

    try:
        parts = message.text.split()
        if len(parts) != 2 or not parts[1].isdigit():
            await message.reply_text("**Usage:** `/addadmin user_id`")
            return

        user_id = int(parts[1])
        success = await add_admin_to_db(user_id)

        if success:
            await message.reply_text(f"✅ User `{user_id}` has been added as an admin.")
        else:
            await message.reply_text(f"⚠️ User `{user_id}` is already an admin.")

    except Exception as e:
        await message.reply_text(f"🔥 Error: `{str(e)}`")



@Client.on_message(filters.command("rmadmin") & filters.private)
async def remove_admin_cmd(client, message: Message):
    try:
        user_id = message.from_user.id
        if user_id != OWNER_ID:
            return await message.reply_text("__Only my Owner can remove admins.__")

        if len(message.command) != 2:
            return await message.reply_text("**Usage:** `/rmadmin user_id`")

        target_id = int(message.command[1])

        removed = await remove_admin_from_db(target_id)
        if removed:
            await message.reply_text(f"✅ User `{target_id}` has been removed from admin list.")
        else:
            await message.reply_text(f"⚠️ User `{target_id}` is not in the admin list.")

    except Exception as e:
        await message.reply_text(f"❌ Error: `{str(e)}`")




@Client.on_message(filters.command("adminlist") & filters.private)
async def list_admins_cmd(client, message: Message):
    try:
        user_id = message.from_user.id
        if user_id != OWNER_ID:
            return await message.reply_text("__Only Owner can view the admin list!__")

        admin_ids = await get_all_admin_ids()

        if not admin_ids:
            await message.reply_text("__No admins found in the list.__")
            return

        text = "**🔐 List of Admins:**\n"
        text += "\n".join([f"- `{uid}`" for uid in admin_ids])
        await message.reply_text(text)

    except Exception as e:
        await message.reply_text(f"❌ Error: `{str(e)}`")