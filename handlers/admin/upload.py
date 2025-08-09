# © @ThealphaBotz [2021-2025]
from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from utils import ButtonManager, humanbytes
import config
import uuid
from handlers.admin.manage_admin import get_all_admin_ids

db = Database()
button_manager = ButtonManager()

async def process_single_file(client: Client, file_message: Message, status_msg: Message = None):
    try:
        forwarded_msg = await file_message.copy(config.DB_CHANNEL_ID)
        
        file_data = {
            "file_id": None,
            "file_name": "Unknown",
            "file_size": 0,
            "file_type": None,
            "uuid": str(uuid.uuid4()),
            "uploader_id": file_message.from_user.id,
            "message_id": forwarded_msg.id,
            "auto_delete": True,
            "auto_delete_time": getattr(config, 'DEFAULT_AUTO_DELETE', 30)
        }

        if file_message.document:
            file_data.update({
                "file_id": file_message.document.file_id,
                "file_name": file_message.document.file_name or "document",
                "file_size": file_message.document.file_size,
                "file_type": "document"
            })
        elif file_message.video:
            file_data.update({
                "file_id": file_message.video.file_id,
                "file_name": file_message.video.file_name or "video.mp4",
                "file_size": file_message.video.file_size,
                "file_type": "video"
            })
        elif file_message.audio:
            file_data.update({
                "file_id": file_message.audio.file_id,
                "file_name": file_message.audio.file_name or "audio",
                "file_size": file_message.audio.file_size,
                "file_type": "audio"
            })
        elif file_message.photo:
            file_data.update({
                "file_id": file_message.photo.file_id,
                "file_name": f"photo_{file_data['uuid']}.jpg",
                "file_size": file_message.photo.file_size,
                "file_type": "photo"
            })
        elif file_message.voice:
            file_data.update({
                "file_id": file_message.voice.file_id,
                "file_name": f"voice_{file_data['uuid']}.ogg",
                "file_size": file_message.voice.file_size,
                "file_type": "voice"
            })
        elif file_message.video_note:
            file_data.update({
                "file_id": file_message.video_note.file_id,
                "file_name": f"video_note_{file_data['uuid']}.mp4",
                "file_size": file_message.video_note.file_size,
                "file_type": "video_note"
            })
        elif file_message.animation:
            file_data.update({
                "file_id": file_message.animation.file_id,
                "file_name": file_message.animation.file_name or f"animation_{file_data['uuid']}.gif",
                "file_size": file_message.animation.file_size,
                "file_type": "animation"
            })
        else:
            if status_msg:
                await status_msg.edit_text("❌ **Unsupported file type!**")
            return None

        if not file_data["file_id"]:
            if status_msg:
                await status_msg.edit_text("❌ **Could not process file!**")
            return None

        if file_data["file_size"] and file_data["file_size"] > config.MAX_FILE_SIZE:
            if status_msg:
                await status_msg.edit_text(f"❌ **File too large!**\nMaximum size: {humanbytes(config.MAX_FILE_SIZE)}")
            return None

        file_uuid = await db.add_file(file_data)
        share_link = f"https://t.me/{config.BOT_USERNAME}?start={file_uuid}"
        chat_share_link = f"https://t.me/share/url?url={share_link}"
        
        return {
            "file_name": file_data['file_name'],
            "file_size": file_data['file_size'],
            "file_type": file_data['file_type'],
            "share_link": share_link,
            "chat_share_link": chat_share_link,
            "uuid": file_uuid
        }

    except Exception as e:
        if status_msg:
            error_text = (
                "❌ **Upload Failed**\n\n"
                f"Error: {str(e)}\n\n"
                "Please try again or contact support if the issue persists."
            )
            await status_msg.edit_text(error_text)
        return None

async def process_upload(client: Client, message: Message, replied_msg=None):
    from_user_id = message.from_user.id
    admins = await get_all_admin_ids()

    if from_user_id not in admins:
        return await message.reply_text("__You are not authorized to upload files!__")
    
    messages_to_process = []
    if replied_msg:
        messages_to_process.append(replied_msg)
    elif message.media_group_id:
        async for m in client.get_media_group(message.chat.id, message.id):
            messages_to_process.append(m)
    else:
        messages_to_process.append(message)
    
    if not messages_to_process:
        await message.reply_text("❌ No valid files found!")
        return
    
    status_msg = await message.reply_text(
        f"🔄 **Processing Upload**\n\n⏳ Processing {len(messages_to_process)} file(s)..."
    )
    
    results = []
    for msg in messages_to_process:
        result = await process_single_file(client, msg)
        if result:
            results.append(result)
    
    if not results:
        await status_msg.edit_text("❌ **No files could be processed!**")
        return
    
    success_text = f"✅ **Successfully uploaded {len(results)} file(s)**\n\n"
    
    for idx, result in enumerate(results, 1):
        success_text += (
            f"**File {idx}:**\n"
            f"📁 **Name:** `{result['file_name']}`\n"
            f"📊 **Size:** {humanbytes(result['file_size'])}\n"
            f"📎 **Type:** {result['file_type']}\n"
            f"🔗 **Link:** `{result['share_link']}`\n\n"
        )
    
    success_text += f"⏱ **Auto-Delete:** {getattr(config, 'DEFAULT_AUTO_DELETE', 30)} minutes\n"
    success_text += f"💡 Use `Check .env file of your Repo to change auto-delete time"
    
    if len(results) == 1:
        await status_msg.edit_text(
            success_text,
            reply_markup=button_manager.file_button(results[0]['chat_share_link'], results[0]['uuid'])
        )
    else:
        await status_msg.edit_text(success_text)

@Client.on_message(filters.command("upload") & filters.reply)
async def upload_command(client: Client, message: Message):
    await process_upload(client, message, message.reply_to_message)

@Client.on_message(
    filters.private & 
    (filters.document | filters.video | filters.audio | filters.photo | 
     filters.voice | filters.video_note | filters.animation)
)
async def direct_upload(client: Client, message: Message):
    await process_upload(client, message)
