# © @TheAlphaBotz [2021-2025]
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from database import Database
from utils import ButtonManager, humanbytes
import config
import uuid
from datetime import datetime
import pytz
from handlers.admin.manage_admin import get_all_admin_ids
import asyncio
import re

db = Database()
button_manager = ButtonManager()
batch_users = {}

def extract_episode_number(filename):
    if not filename:
        return float('inf')
    
    patterns = [
        r'[Ee](\d+)',
        r'[Ee]pisode\s*(\d+)',
        r'[Ee]p\s*(\d+)',
        r'S\d+[Ee](\d+)',
        r'\[E(\d+)\]',
        r'-E(\d+)-',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            return int(match.group(1))
    
    return float('inf')

@Client.on_message(filters.command("batch") & filters.private)
async def batch_command(client: Client, message: Message):
    from_user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if from_user_id not in admins:
        return await message.reply_text("__Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜꜱᴇ ʙᴀᴛᴄʜ ᴍᴏᴅᴇ!__")
    
    user_id = message.from_user.id
    batch_users[user_id] = {
        "files": [],
        "status_msg": None,
        "processing_queue": [],
        "is_processing": False,
        "processed_count": 0
    }
    
    await message.reply_text(
        "📦 **Bᴀᴛᴄʜ Mᴏᴅᴇ Aᴄᴛɪᴠᴀᴛᴇᴅ!**\n\n"
        "• Sᴇɴᴅ ᴍᴜʟᴛɪᴘʟᴇ ꜰɪʟᴇꜱ ᴏɴᴇ ʙʏ ᴏɴᴇ\n"
        "• Eᴀᴄʜ ꜰɪʟᴇ ᴡɪʟʟ ʙᴇ ᴘʀᴏᴄᴇꜱꜱᴇᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ\n"
        "• Uꜱᴇ /done ᴡʜᴇɴ ꜰɪɴɪꜱʜᴇᴅ ᴛᴏ ɢᴇᴛ ʙᴀᴛᴄʜ ʟɪɴᴋ\n"
        "• Uꜱᴇ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ ʙᴀᴛᴄʜ ᴍᴏᴅᴇ"
    )

async def process_file_sequentially(client: Client, user_id: int):
    if batch_users[user_id]["is_processing"]:
        return
    
    batch_users[user_id]["is_processing"] = True
    
    while batch_users[user_id]["processing_queue"]:
        message_data = batch_users[user_id]["processing_queue"].pop(0)
        message = message_data["message"]
        
        try:
            max_retries = 3
            retry_count = 0
            copied_msg = None
            
            while retry_count < max_retries:
                try:
                    copied_msg = await message.copy(config.DB_CHANNEL_ID)
                    break
                except FloodWait as e:
                    retry_count += 1
                    wait_time = e.value
                    await message.reply_text(f"⏳ Fʟᴏᴏᴅᴡᴀɪᴛ {wait_time} ꜱᴇᴄᴏɴᴅꜱ. Rᴇꜱᴜᴍɪɴɢ...")
                    await asyncio.sleep(wait_time)
                except Exception as e:
                    if retry_count >= max_retries - 1:
                        raise
                    await asyncio.sleep(2)
            
            if not copied_msg:
                await message.reply_text("❌ Fᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇꜱꜱ ꜰɪʟᴇ ᴀꜰᴛᴇʀ ʀᴇᴛʀɪᴇꜱ")
                continue
            
            file_data = {
                "file_id": None,
                "file_name": "Unknown",
                "file_size": 0,
                "file_type": None,
                "uuid": str(uuid.uuid4()),
                "uploader_id": user_id,
                "message_id": copied_msg.id,
                "auto_delete": True,
                "auto_delete_time": getattr(config, 'DEFAULT_AUTO_DELETE', 30),
                "sequence_number": len(batch_users[user_id]["files"]) + 1
            }

            if message.document:
                file_data.update({
                    "file_id": message.document.file_id,
                    "file_name": message.document.file_name or "document",
                    "file_size": message.document.file_size,
                    "file_type": "document"
                })
            elif message.video:
                file_data.update({
                    "file_id": message.video.file_id,
                    "file_name": message.video.file_name or "video.mp4",
                    "file_size": message.video.file_size,
                    "file_type": "video"
                })
            elif message.audio:
                file_data.update({
                    "file_id": message.audio.file_id,
                    "file_name": message.audio.file_name or "audio",
                    "file_size": message.audio.file_size,
                    "file_type": "audio"
                })
            elif message.photo:
                file_data.update({
                    "file_id": message.photo.file_id,
                    "file_name": f"photo_{file_data['uuid']}.jpg",
                    "file_size": message.photo.file_size,
                    "file_type": "photo"
                })
            else:
                await message.reply_text("❌ Uɴꜱᴜᴘᴘᴏʀᴛᴇᴅ ꜰɪʟᴇ ᴛʏᴘᴇ!")
                continue

            if not file_data["file_id"]:
                await message.reply_text("❌ Cᴏᴜʟᴅ ɴᴏᴛ ᴘʀᴏᴄᴇꜱꜱ ꜰɪʟᴇ!")
                continue

            if file_data["file_size"] > config.MAX_FILE_SIZE:
                await message.reply_text(f"❌ Fɪʟᴇ ᴛᴏᴏ ʟᴀʀɢᴇ!\nMᴀxɪᴍᴜᴍ ꜱɪᴢᴇ: {humanbytes(config.MAX_FILE_SIZE)}")
                continue

            file_uuid = await db.add_file(file_data)
            batch_users[user_id]["files"].append(file_uuid)
            batch_users[user_id]["processed_count"] += 1
            
            await message.reply_text(f"✅ Fɪʟᴇ Aᴅᴅᴇᴅ Iɴ Qᴜᴇᴜᴇ ({batch_users[user_id]['processed_count']})")

        except FloodWait as e:
            batch_users[user_id]["processing_queue"].insert(0, message_data)
            wait_time = e.value
            await message.reply_text(f"⏳ Fʟᴏᴏᴅᴡᴀɪᴛ {wait_time} ꜱᴇᴄᴏɴᴅꜱ. Rᴇꜱᴜᴍɪɴɢ...")
            await asyncio.sleep(wait_time)
            continue
            
        except Exception as e:
            await message.reply_text(
                f"❌ Pʀᴏᴄᴇꜱꜱɪɴɢ Fᴀɪʟᴇᴅ\n\n"
                f"Eʀʀᴏʀ: {str(e)}"
            )
        
        await asyncio.sleep(0.5)
    
    batch_users[user_id]["is_processing"] = False

@Client.on_message(~filters.command(["batch", "done", "cancel", "qu", "qupload", "qdone", "qud", "qcancel", "qmode"]) & filters.private)
async def handle_batch_file(client: Client, message: Message):
    user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if user_id not in admins:
        return
    
    try:
        from handlers.admin.qupload import is_qupload_active, handle_qupload_file_internal
        
        if is_qupload_active(user_id):
            await handle_qupload_file_internal(client, message, user_id)
            return
    except ImportError:
        pass
    
    if user_id not in batch_users:
        return
    
    batch_users[user_id]["processing_queue"].append({
        "message": message
    })
    
    asyncio.create_task(process_file_sequentially(client, user_id))

@Client.on_message(filters.command("done") & filters.private)
async def done_command(client: Client, message: Message):
    user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if user_id not in admins:
        return
    
    try:
        from handlers.admin.qupload import is_qupload_active
        if is_qupload_active(user_id):
            return
    except ImportError:
        pass
        
    if user_id not in batch_users:
        await message.reply_text("⚠️ Bᴀᴛᴄʜ ᴍᴏᴅᴇ ɪꜱ ɴᴏᴛ ᴀᴄᴛɪᴠᴇ! Uꜱᴇ /batch ᴛᴏ ꜱᴛᴀʀᴛ.")
        return
    
    status_msg = await message.reply_text("⏳ Wᴀɪᴛɪɴɢ ꜰᴏʀ ᴀʟʟ ꜰɪʟᴇꜱ ᴛᴏ ᴘʀᴏᴄᴇꜱꜱ...")
    
    while batch_users[user_id]["processing_queue"] or batch_users[user_id]["is_processing"]:
        await asyncio.sleep(1)
        
    if not batch_users[user_id]["files"]:
        await status_msg.edit_text("❌ Nᴏ ꜰɪʟᴇꜱ ɪɴ ʙᴀᴛᴄʜ! Sᴇɴᴅ ꜱᴏᴍᴇ ꜰɪʟᴇꜱ ꜰɪʀꜱᴛ.")
        return
    
    try:
        await status_msg.edit_text("🔄 Cʀᴇᴀᴛɪɴɢ Bᴀᴛᴄʜ Lɪɴᴋ & Sᴏʀᴛɪɴɢ Eᴘɪꜱᴏᴅᴇꜱ...")
        
        file_data_list = []
        for file_uuid in batch_users[user_id]["files"]:
            file_data = await db.files_collection.find_one({"uuid": file_uuid})
            if file_data:
                file_data_list.append(file_data)
        
        sorted_files = sorted(file_data_list, key=lambda x: extract_episode_number(x.get("file_name", "")))
        
        sorted_file_uuids = [file_data["uuid"] for file_data in sorted_files]
        
        batch_uuid = str(uuid.uuid4())
        batch_data = {
            "uuid": batch_uuid,
            "files": sorted_file_uuids,
            "uploader_id": user_id,
            "created_at": datetime.now(pytz.UTC),
            "file_count": len(sorted_file_uuids),
            "auto_delete": True,
            "auto_delete_time": getattr(config, 'DEFAULT_AUTO_DELETE', 30)
        }
        
        await db.batch_collection.insert_one(batch_data)
        batch_link = f"https://t.me/{config.BOT_USERNAME}?start=batch_{batch_uuid}"
        
        await status_msg.edit_text(
            f"✅ **Bᴀᴛᴄʜ Cʀᴇᴀᴛᴇᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ**\n\n"
            f"📁 **Tᴏᴛᴀʟ Fɪʟᴇꜱ:** {len(sorted_file_uuids)}\n"
            f"⏱ **Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ:** {batch_data['auto_delete_time']} ᴍɪɴᴜᴛᴇꜱ\n"
            f"🔗 **Bᴀᴛᴄʜ Lɪɴᴋ:** `{batch_link}`"
        )
        
        del batch_users[user_id]
        
    except Exception as e:
        await status_msg.edit_text(
            f"❌ **Bᴀᴛᴄʜ Cʀᴇᴀᴛɪᴏɴ Fᴀɪʟᴇᴅ**\n\n"
            f"Eʀʀᴏʀ: {str(e)}"
        )
        if user_id in batch_users:
            del batch_users[user_id]

@Client.on_message(filters.command("start") & filters.regex(r"^/start batch_"))
async def handle_batch_start(client: Client, message: Message):
    try:
        batch_uuid = message.text.split("_")[1]
        batch_data = await db.batch_collection.find_one({"uuid": batch_uuid})
        
        if not batch_data:
            await message.reply_text("❌ Bᴀᴛᴄʜ ɴᴏᴛ ꜰᴏᴜɴᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ!")
            return
        
        status_msg = await message.reply_text("🔄 Sᴇɴᴅɪɴɢ ꜰɪʟᴇꜱ...")
        
        sent_count = 0
        for file_uuid in batch_data["files"]:
            file_data = await db.files_collection.find_one({"uuid": file_uuid})
            if file_data:
                try:
                    max_retries = 3
                    retry_count = 0
                    
                    while retry_count < max_retries:
                        try:
                            await client.copy_message(
                                chat_id=message.chat.id,
                                from_chat_id=config.DB_CHANNEL_ID,
                                message_id=file_data["message_id"]
                            )
                            sent_count += 1
                            break
                        except FloodWait as e:
                            wait_time = e.value
                            await status_msg.edit_text(
                                f"⏳ Fʟᴏᴏᴅᴡᴀɪᴛ {wait_time} ꜱᴇᴄᴏɴᴅꜱ. Rᴇꜱᴜᴍɪɴɢ...\n\n"
                                f"Sᴇɴᴛ: {sent_count}/{len(batch_data['files'])}"
                            )
                            await asyncio.sleep(wait_time)
                            retry_count += 1
                        except Exception as e:
                            if retry_count >= max_retries - 1:
                                raise
                            await asyncio.sleep(2)
                            retry_count += 1
                    
                    await asyncio.sleep(0.3)
                    
                except Exception as e:
                    await message.reply_text(f"❌ Eʀʀᴏʀ ꜱᴇɴᴅɪɴɢ: {file_data['file_name']}")
        
        await status_msg.edit_text(f"✅ Aʟʟ ꜰɪʟᴇꜱ ꜱᴇɴᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ! ({sent_count}/{len(batch_data['files'])})")
        
    except Exception as e:
        await message.reply_text(
            f"❌ **Dᴏᴡɴʟᴏᴀᴅ Fᴀɪʟᴇᴅ**\n\n"
            f"Eʀʀᴏʀ: {str(e)}"
        )

@Client.on_message(filters.command("cancel") & filters.private)
async def cancel_command(client: Client, message: Message):
    user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if user_id not in admins:
        return
        
    if user_id in batch_users:
        del batch_users[user_id]
        await message.reply_text("❌ Bᴀᴛᴄʜ ᴍᴏᴅᴇ ᴄᴀɴᴄᴇʟʟᴇᴅ!")
    else:
        await message.reply_text("⚠️ Bᴀᴛᴄʜ ᴍᴏᴅᴇ ɪꜱ ɴᴏᴛ ᴀᴄᴛɪᴠᴇ!")
