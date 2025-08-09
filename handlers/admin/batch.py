# © @TheAlphaBotz [2021-2025]
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
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
        return await message.reply_text("__You are not authorized to use batch mode!__")
    
    user_id = message.from_user.id
    batch_users[user_id] = {
        "files": [],
        "status_msg": None,
        "processing_queue": [],
        "is_processing": False
    }
    
    await message.reply_text(
        "📦 **Batch Mode Activated!**\n\n"
        "• Send multiple files one by one\n"
        "• Each file will be processed automatically\n"
        "• Use /done when finished to get batch link\n"
        "• Use /cancel to cancel batch mode"
    )

async def process_file_sequentially(client: Client, user_id: int):
    if batch_users[user_id]["is_processing"]:
        return
    
    batch_users[user_id]["is_processing"] = True
    
    while batch_users[user_id]["processing_queue"]:
        message_data = batch_users[user_id]["processing_queue"].pop(0)
        message = message_data["message"]
        status_msg = message_data["status_msg"]
        
        try:
            copied_msg = await message.copy(config.DB_CHANNEL_ID)
            
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
                await status_msg.edit_text("❌ **Unsupported file type!**")
                continue

            if not file_data["file_id"]:
                await status_msg.edit_text("❌ **Could not process file!**")
                continue

            if file_data["file_size"] > config.MAX_FILE_SIZE:
                await status_msg.edit_text(f"❌ **File too large!**\nMaximum size: {humanbytes(config.MAX_FILE_SIZE)}")
                continue

            file_uuid = await db.add_file(file_data)
            batch_users[user_id]["files"].append(file_uuid)
            
            await status_msg.edit_text(
                f"✅ **File {len(batch_users[user_id]['files'])} Added to Batch**\n\n"
                f"📁 **Name:** `{file_data['file_name']}`\n"
                f"📊 **Size:** {humanbytes(file_data['file_size'])}\n"
                f"📎 **Type:** {file_data['file_type']}\n"
                f"🔢 **Sequence:** {file_data['sequence_number']}\n\n"
                f"Send more files or use /done to finish batch."
            )

        except Exception as e:
            await status_msg.edit_text(
                "❌ **Processing Failed**\n\n"
                f"Error: {str(e)}\n\n"
                "Please try again or contact support."
            )
        
        await asyncio.sleep(0.5)
    
    batch_users[user_id]["is_processing"] = False

@Client.on_message(~filters.command(["batch", "done", "cancel"]) & filters.private)
async def handle_batch_file(client: Client, message: Message):
    user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if user_id not in admins:
        return
    
    if user_id not in batch_users:
        return
    
    status_msg = await message.reply_text("🔄 **Queued for Processing**\n\n⏳ Waiting in sequence...")
    
    batch_users[user_id]["processing_queue"].append({
        "message": message,
        "status_msg": status_msg
    })
    
    asyncio.create_task(process_file_sequentially(client, user_id))

@Client.on_message(filters.command("done") & filters.private)
async def done_command(client: Client, message: Message):
    user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if user_id not in admins:
        return
        
    if user_id not in batch_users:
        await message.reply_text("⚠️ Batch mode is not active! Use /batch to start.")
        return
    
    while batch_users[user_id]["processing_queue"] or batch_users[user_id]["is_processing"]:
        await asyncio.sleep(1)
        
    if not batch_users[user_id]["files"]:
        await message.reply_text("❌ No files in batch! Send some files first.")
        return
    
    try:
        status_msg = await message.reply_text("🔄 **Creating Batch Link & Sorting Episodes**\n\n⏳ Please wait...")
        
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

        chat_share_link = f"https://t.me/share/url?url={batch_link}"
        
        await status_msg.edit_text(
            f"✅ **Batch Created Successfully**\n\n"
            f"📁 **Total Files:** {len(sorted_file_uuids)}\n"
            f"⏱ **Auto-Delete:** {batch_data['auto_delete_time']} minutes\n"
            f"🔗 **Batch Link:** `{batch_link}`"
        )
        
        del batch_users[user_id]
        
    except Exception as e:
        await status_msg.edit_text(
            "❌ **Batch Creation Failed**\n\n"
            f"Error: {str(e)}\n\n"
            "Please try again or contact support."
        )
        if user_id in batch_users:
            del batch_users[user_id]

@Client.on_message(filters.command("start") & filters.regex(r"^/start batch_"))
async def handle_batch_start(client: Client, message: Message):
    try:
        batch_uuid = message.text.split("_")[1]
        batch_data = await db.batch_collection.find_one({"uuid": batch_uuid})
        
        if not batch_data:
            await message.reply_text("❌ Batch not found or expired!")
            return
        
        status_msg = await message.reply_text("🔄 **Processing Batch Download**\n\n⏳ Please wait...")
        
        for file_uuid in batch_data["files"]:
            file_data = await db.files_collection.find_one({"uuid": file_uuid})
            if file_data:
                try:
                    await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=config.DB_CHANNEL_ID,
                        message_id=file_data["message_id"]
                    )
                    await asyncio.sleep(0.3)
                except Exception as e:
                    await message.reply_text(f"❌ Error sending file: {file_data['file_name']}")
        
        await status_msg.edit_text("✅ **All files sent successfully in order!**")
        
    except Exception as e:
        await message.reply_text(
            "❌ **Download Failed**\n\n"
            f"Error: {str(e)}\n\n"
            "Please try again or contact support."
        )

@Client.on_message(filters.command("cancel") & filters.private)
async def cancel_command(client: Client, message: Message):
    user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if user_id not in admins:
        return
        
    if user_id in batch_users:
        del batch_users[user_id]
        await message.reply_text("❌ Batch mode cancelled!")
    else:
        await message.reply_text("⚠️ Batch mode is not active!")
