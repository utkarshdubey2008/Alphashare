# © @TheAlphaBotz [2021-2025]
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait
from database import Database
from utils import humanbytes
import config
import uuid
from datetime import datetime
import pytz
from handlers.admin.manage_admin import get_all_admin_ids
import asyncio
import re

db = Database()
qupload_users = {}
qupload_modes = {}

def extract_quality(text, source="filename"):
    if not text:
        return "Unknown"
    
    text_lower = text.lower()
    
    quality_patterns = [
        (r'\b(2160p|4k)\b', '2160p'),
        (r'\b1440p\b', '1440p'),
        (r'\b1080p\b', '1080p'),
        (r'\b720p\b', '720p'),
        (r'\b480p\b', '480p'),
        (r'\b360p\b', '360p'),
        (r'\b240p\b', '240p'),
        (r'\b(hd[\s\-_.]?rip|hdrip)\b', 'HDrip'),
        (r'\b(web[\s\-_.]?rip|webrip)\b', 'WEBrip'),
        (r'\b(web[\s\-_.]?dl|webdl|web-dl)\b', 'WEB-DL'),
        (r'\b(blu[\s\-_.]?ray|bluray|blu-ray)\b', 'BluRay'),
        (r'\b(dvd[\s\-_.]?rip|dvdrip)\b', 'DVDrip'),
        (r'\b(hdtv)\b', 'HDTV'),
        (r'\b(cam)\b', 'CAM'),
        (r'\b(ts|telesync)\b', 'TS'),
    ]
    
    for pattern, quality_name in quality_patterns:
        if re.search(pattern, text_lower):
            return quality_name
    
    return "Unknown"

@Client.on_message(filters.command("qmode") & filters.private)
async def qmode_command(client: Client, message: Message):
    from_user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if from_user_id not in admins:
        return await message.reply_text("__Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜꜱᴇ Qᴜᴀʟɪᴛʏ Mᴏᴅᴇ ꜱᴇᴛᴛɪɴɢꜱ!__")
    
    current_mode = qupload_modes.get(from_user_id, "filename")
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Fɪʟᴇɴᴀᴍᴇ" if current_mode == "filename" else "Fɪʟᴇɴᴀᴍᴇ",
                callback_data="qmode_filename"
            ),
            InlineKeyboardButton(
                "✅ Cᴀᴘᴛɪᴏɴ" if current_mode == "caption" else "Cᴀᴘᴛɪᴏɴ",
                callback_data="qmode_caption"
            )
        ]
    ])
    
    await message.reply_text(
        "🎬 **Qᴜᴀʟɪᴛʏ Exᴛʀᴀᴄᴛɪᴏɴ Mᴏᴅᴇ**\n\n"
        f"**Cᴜʀʀᴇɴᴛ Mᴏᴅᴇ:** `{current_mode.title()}`\n\n"
        "**Fɪʟᴇɴᴀᴍᴇ:** Exᴛʀᴀᴄᴛ ǫᴜᴀʟɪᴛʏ ꜰʀᴏᴍ ꜰɪʟᴇ ɴᴀᴍᴇ\n"
        "**Cᴀᴘᴛɪᴏɴ:** Exᴛʀᴀᴄᴛ ǫᴜᴀʟɪᴛʏ ꜰʀᴏᴍ ꜰɪʟᴇ ᴄᴀᴘᴛɪᴏɴ\n\n"
        "Sᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴘʀᴇꜰᴇʀʀᴇᴅ ᴍᴏᴅᴇ:",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex(r"^qmode_"))
async def qmode_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    admins = await get_all_admin_ids()
    if user_id not in admins:
        await callback_query.answer("Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ!", show_alert=True)
        return
    
    mode = callback_query.data.split("_")[1]
    qupload_modes[user_id] = mode
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Fɪʟᴇɴᴀᴍᴇ" if mode == "filename" else "Fɪʟᴇɴᴀᴍᴇ",
                callback_data="qmode_filename"
            ),
            InlineKeyboardButton(
                "✅ Cᴀᴘᴛɪᴏɴ" if mode == "caption" else "Cᴀᴘᴛɪᴏɴ",
                callback_data="qmode_caption"
            )
        ]
    ])
    
    await callback_query.edit_message_text(
        "🎬 **Qᴜᴀʟɪᴛʏ Exᴛʀᴀᴄᴛɪᴏɴ Mᴏᴅᴇ**\n\n"
        f"**Cᴜʀʀᴇɴᴛ Mᴏᴅᴇ:** `{mode.title()}`\n\n"
        "**Fɪʟᴇɴᴀᴍᴇ:** Exᴛʀᴀᴄᴛ ǫᴜᴀʟɪᴛʏ ꜰʀᴏᴍ ꜰɪʟᴇ ɴᴀᴍᴇ\n"
        "**Cᴀᴘᴛɪᴏɴ:** Exᴛʀᴀᴄᴛ ǫᴜᴀʟɪᴛʏ ꜰʀᴏᴍ ꜰɪʟᴇ ᴄᴀᴘᴛɪᴏɴ\n\n"
        "Sᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴘʀᴇꜰᴇʀʀᴇᴅ ᴍᴏᴅᴇ:",
        reply_markup=keyboard
    )
    
    await callback_query.answer(f"✅ Mᴏᴅᴇ ꜱᴇᴛ ᴛᴏ: {mode.title()}")

@Client.on_message(filters.command(["qu", "qupload"]) & filters.private)
async def qupload_command(client: Client, message: Message):
    from_user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if from_user_id not in admins:
        return await message.reply_text("__Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜꜱᴇ Qᴜᴀʟɪᴛʏ Uᴘʟᴏᴀᴅ ᴍᴏᴅᴇ!__")
    
    user_id = message.from_user.id
    qupload_users[user_id] = {
        "files": {},
        "processing_queue": [],
        "is_processing": False,
        "processed_count": 0
    }
    
    mode = qupload_modes.get(user_id, "filename")
    
    await message.reply_text(
        "🎬 **Qᴜᴀʟɪᴛʏ Uᴘʟᴏᴀᴅ Mᴏᴅᴇ Aᴄᴛɪᴠᴀᴛᴇᴅ!**\n\n"
        f"📌 **Exᴛʀᴀᴄᴛɪᴏɴ Mᴏᴅᴇ:** `{mode.title()}`\n"
        "• Sᴇɴᴅ ꜰɪʟᴇꜱ ᴡɪᴛʜ ǫᴜᴀʟɪᴛʏ ɪɴ ɴᴀᴍᴇ/ᴄᴀᴘᴛɪᴏɴ\n"
        "• Fɪʟᴇꜱ ᴡɪʟʟ ʙᴇ ɢʀᴏᴜᴘᴇᴅ ʙʏ ǫᴜᴀʟɪᴛʏ\n"
        "• Uꜱᴇ /qdone ᴏʀ /qud ᴛᴏ ɢᴇᴛ ʟɪɴᴋꜱ\n"
        "• Uꜱᴇ /qcancel ᴛᴏ ᴄᴀɴᴄᴇʟ\n"
        "• Uꜱᴇ /qmode ᴛᴏ ᴄʜᴀɴɢᴇ ᴍᴏᴅᴇ"
    )

async def process_qupload_file(client: Client, user_id: int):
    if qupload_users[user_id]["is_processing"]:
        return
    
    qupload_users[user_id]["is_processing"] = True
    
    while qupload_users[user_id]["processing_queue"]:
        message_data = qupload_users[user_id]["processing_queue"].pop(0)
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

            mode = qupload_modes.get(user_id, "filename")
            
            if mode == "caption" and message.caption:
                quality = extract_quality(message.caption, "caption")
            else:
                quality = extract_quality(file_data["file_name"], "filename")
            
            file_data["quality"] = quality
            
            file_uuid = await db.add_file(file_data)
            
            if quality not in qupload_users[user_id]["files"]:
                qupload_users[user_id]["files"][quality] = []
            
            qupload_users[user_id]["files"][quality].append(file_uuid)
            qupload_users[user_id]["processed_count"] += 1
            
            await message.reply_text(
                f"✅ **Fɪʟᴇ Aᴅᴅᴇᴅ** ({qupload_users[user_id]['processed_count']})\n"
                f"🎬 **Qᴜᴀʟɪᴛʏ:** {quality}"
            )

        except FloodWait as e:
            qupload_users[user_id]["processing_queue"].insert(0, message_data)
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
    
    qupload_users[user_id]["is_processing"] = False

def is_qupload_active(user_id: int) -> bool:
    return user_id in qupload_users

async def handle_qupload_file_internal(client: Client, message: Message, user_id: int):
    qupload_users[user_id]["processing_queue"].append({
        "message": message
    })
    asyncio.create_task(process_qupload_file(client, user_id))

async def handle_qupload_done_internal(client: Client, message: Message, user_id: int):
    await qupload_done_command(client, message)

@Client.on_message(filters.command(["qdone", "qud"]) & filters.private)
async def qupload_done_command(client: Client, message: Message):
    user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if user_id not in admins:
        return
    
    if user_id not in qupload_users:
        await message.reply_text("⚠️ Qᴜᴀʟɪᴛʏ Uᴘʟᴏᴀᴅ ᴍᴏᴅᴇ ɪꜱ ɴᴏᴛ ᴀᴄᴛɪᴠᴇ! Uꜱᴇ /qu ᴛᴏ ꜱᴛᴀʀᴛ.")
        return
    
    status_msg = await message.reply_text("⏳ Wᴀɪᴛɪɴɢ ꜰᴏʀ ᴀʟʟ ꜰɪʟᴇꜱ ᴛᴏ ᴘʀᴏᴄᴇꜱꜱ...")
    
    while qupload_users[user_id]["processing_queue"] or qupload_users[user_id]["is_processing"]:
        await asyncio.sleep(1)
    
    if not qupload_users[user_id]["files"]:
        await status_msg.edit_text("❌ Nᴏ ꜰɪʟᴇꜱ ɪɴ ǫᴜᴀʟɪᴛʏ ᴜᴘʟᴏᴀᴅ! Sᴇɴᴅ ꜱᴏᴍᴇ ꜰɪʟᴇꜱ ꜰɪʀꜱᴛ.")
        del qupload_users[user_id]
        return
    
    try:
        await status_msg.edit_text("🔄 Gᴇɴᴇʀᴀᴛɪɴɢ Qᴜᴀʟɪᴛʏ-Bᴀꜱᴇᴅ Lɪɴᴋꜱ...")
        
        quality_order = {
            '2160p': 0, '4k': 0,
            '1440p': 1,
            '1080p': 2,
            '720p': 3,
            '480p': 4,
            '360p': 5,
            '240p': 6,
            'BluRay': 7,
            'WEB-DL': 8,
            'WEBrip': 9,
            'HDrip': 10,
            'HDTV': 11,
            'DVDrip': 12,
            'TS': 13,
            'CAM': 14,
            'Unknown': 15
        }
        
        sorted_qualities = sorted(
            qupload_users[user_id]["files"].keys(),
            key=lambda x: quality_order.get(x, 99)
        )
        
        quality_links = {}
        total_files = 0
        
        for quality in sorted_qualities:
            file_uuids = qupload_users[user_id]["files"][quality]
            total_files += len(file_uuids)
            
            if len(file_uuids) == 1:
                file_uuid = file_uuids[0]
                link = f"https://t.me/{config.BOT_USERNAME}?start={file_uuid}"
                quality_links[quality] = link
            else:
                batch_uuid = str(uuid.uuid4())
                batch_data = {
                    "uuid": batch_uuid,
                    "files": file_uuids,
                    "uploader_id": user_id,
                    "created_at": datetime.now(pytz.UTC),
                    "file_count": len(file_uuids),
                    "auto_delete": True,
                    "auto_delete_time": getattr(config, 'DEFAULT_AUTO_DELETE', 30),
                    "quality": quality
                }
                await db.batch_collection.insert_one(batch_data)
                
                link = f"https://t.me/{config.BOT_USERNAME}?start=batch_{batch_uuid}"
                quality_links[quality] = link
        
        resolution_qualities = ['240p', '360p', '480p', '720p', '1080p', '1440p', '2160p', '4k']
        rip_qualities = ['BluRay', 'WEB-DL', 'WEBrip', 'HDrip', 'HDTV', 'DVDrip', 'TS', 'CAM', 'Unknown']
        
        lines = []
        
        res_parts = []
        for quality in resolution_qualities:
            if quality in quality_links:
                res_parts.append(f"{quality} - `{quality_links[quality]}`")
        
        if res_parts:
            lines.append(" | ".join(res_parts))
        
        for quality in rip_qualities:
            if quality in quality_links:
                lines.append(f"{quality} - `{quality_links[quality]}`")
        
        links_text = "\n".join(lines)
        
        response_text = (
            f"✅ **Qᴜᴀʟɪᴛʏ Uᴘʟᴏᴀᴅ Cᴏᴍᴘʟᴇᴛᴇᴅ**\n\n"
            f"📁 **Tᴏᴛᴀʟ Fɪʟᴇꜱ:** {total_files}\n"
            f"🎬 **Qᴜᴀʟɪᴛɪᴇꜱ:** {len(sorted_qualities)}\n\n"
            f"{links_text}"
        )
        
        await status_msg.edit_text(response_text)
        
        del qupload_users[user_id]
        
    except Exception as e:
        await status_msg.edit_text(
            f"❌ **Qᴜᴀʟɪᴛʏ Uᴘʟᴏᴀᴅ Fᴀɪʟᴇᴅ**\n\n"
            f"Eʀʀᴏʀ: {str(e)}"
        )
        if user_id in qupload_users:
            del qupload_users[user_id]

@Client.on_message(filters.command("qcancel") & filters.private)
async def qcancel_command(client: Client, message: Message):
    user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if user_id not in admins:
        return
    
    if user_id in qupload_users:
        del qupload_users[user_id]
        await message.reply_text("❌ Qᴜᴀʟɪᴛʏ Uᴘʟᴏᴀᴅ ᴍᴏᴅᴇ ᴄᴀɴᴄᴇʟʟᴇᴅ!")
    else:
        await message.reply_text("⚠️ Qᴜᴀʟɪᴛʏ Uᴘʟᴏᴀᴅ ᴍᴏᴅᴇ ɪꜱ ɴᴏᴛ ᴀᴄᴛɪᴠᴇ!")
