from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from utils import ButtonManager, humanbytes
import config
import uuid
from handlers.admin.manage_admin import get_all_admin_ids

db = Database()
button_manager = ButtonManager()

@Client.on_message(filters.command("upload") & filters.reply)
async def upload_command(client: Client, message: Message):
    from_user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if from_user_id not in admins:
        return await message.reply_text("__You are not authorized to upload files!__")
    
    replied_msg = message.reply_to_message
    if not replied_msg:
        await message.reply_text("❌ Please reply to a valid file!")
        return
    
    status_msg = await message.reply_text("🔄 **Processing Upload**\n\n⏳ Please wait...")
    
    try:
        forwarded_msg = await replied_msg.forward(config.DB_CHANNEL_ID)
        
        file_data = {
            "file_id": None,
            "file_name": "Unknown",
            "file_size": 0,
            "file_type": None,
            "uuid": str(uuid.uuid4()),
            "uploader_id": message.from_user.id,
            "message_id": forwarded_msg.id,
            "auto_delete": True,
            "auto_delete_time": getattr(config, 'DEFAULT_AUTO_DELETE', 30)
        }

        if replied_msg.document:
            file_data.update({
                "file_id": replied_msg.document.file_id,
                "file_name": replied_msg.document.file_name or "document",
                "file_size": replied_msg.document.file_size,
                "file_type": "document"
            })
        elif replied_msg.video:
            file_data.update({
                "file_id": replied_msg.video.file_id,
                "file_name": replied_msg.video.file_name or "video.mp4",
                "file_size": replied_msg.video.file_size,
                "file_type": "video"
            })
        elif replied_msg.audio:
            file_data.update({
                "file_id": replied_msg.audio.file_id,
                "file_name": replied_msg.audio.file_name or "audio",
                "file_size": replied_msg.audio.file_size,
                "file_type": "audio"
            })
        elif replied_msg.photo:
            file_data.update({
                "file_id": replied_msg.photo.file_id,
                "file_name": f"photo_{file_data['uuid']}.jpg",
                "file_size": replied_msg.photo.file_size,
                "file_type": "photo"
            })
        elif replied_msg.voice:
            file_data.update({
                "file_id": replied_msg.voice.file_id,
                "file_name": f"voice_{file_data['uuid']}.ogg",
                "file_size": replied_msg.voice.file_size,
                "file_type": "voice"
            })
        elif replied_msg.video_note:
            file_data.update({
                "file_id": replied_msg.video_note.file_id,
                "file_name": f"video_note_{file_data['uuid']}.mp4",
                "file_size": replied_msg.video_note.file_size,
                "file_type": "video_note"
            })
        elif replied_msg.animation:
            file_data.update({
                "file_id": replied_msg.animation.file_id,
                "file_name": replied_msg.animation.file_name or f"animation_{file_data['uuid']}.gif",
                "file_size": replied_msg.animation.file_size,
                "file_type": "animation"
            })
        else:
            await status_msg.edit_text("❌ **Unsupported file type!**")
            return

        if not file_data["file_id"]:
            await status_msg.edit_text("❌ **Could not process file!**")
            return

        if file_data["file_size"] and file_data["file_size"] > config.MAX_FILE_SIZE:
            await status_msg.edit_text(f"❌ **File too large!**\nMaximum size: {humanbytes(config.MAX_FILE_SIZE)}")
            return

        file_uuid = await db.add_file(file_data)
        share_link = f"https://t.me/{config.BOT_USERNAME}?start={file_uuid}"
        
        upload_success_text = (
            f"✅ **File Upload Successful**\n\n"
            f"📁 **File Name:** `{file_data['file_name']}`\n"
            f"📊 **Size:** {humanbytes(file_data['file_size'])}\n"
            f"📎 **Type:** {file_data['file_type']}\n"
            f"⏱ **Auto-Delete:** {file_data['auto_delete_time']} minutes\n"
            f"🔗 **Share Link:** `{share_link}`\n\n"
            f"💡 Use `/auto_del <minutes>` to change auto-delete time"
        )
        
        await status_msg.edit_text(
            upload_success_text,
            reply_markup=button_manager.file_button(file_uuid)
        )

    except Exception as e:
        error_text = (
            "❌ **Upload Failed**\n\n"
            f"Error: {str(e)}\n\n"
            "Please try again or contact support if the issue persists."
        )
        await status_msg.edit_text(error_text)
