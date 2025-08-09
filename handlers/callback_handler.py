# © @Thealphabotz [2021-2025]
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import Database
from utils import ButtonManager, humanbytes
import config
import logging
import asyncio
from handlers.utils.message_delete import schedule_message_deletion

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = Database()
button_manager = ButtonManager()

@Client.on_callback_query()
async def callback_handler(client: Client, callback: CallbackQuery):
    try:
        if callback.data == "home":
            await button_manager.show_start(client, callback)
        
        elif callback.data == "help":
            await button_manager.show_help(client, callback)
        
        elif callback.data == "about":
            await button_manager.show_about(client, callback)
        
        elif callback.data.startswith("download_"):
            if not await button_manager.check_force_sub(client, callback.from_user.id):
                await callback.answer(
                    "Please join our channel to download files!",
                    show_alert=True
                )
                return
                
            file_uuid = callback.data.split("_")[1]
            file_data = await db.get_file(file_uuid)
            
            if not file_data:
                await callback.answer("File not found!", show_alert=True)
                return
                
            try:
                status_msg = await callback.message.reply_text(
                    "🔄 Processing Download\n\n⏳ Please wait..."
                )
                
                msg = await client.copy_message(
                    chat_id=callback.message.chat.id,
                    from_chat_id=config.DB_CHANNEL_ID,
                    message_id=file_data["message_id"],
                    protect_content=config.PRIVACY_MODE
                )
                await db.increment_downloads(file_uuid)
                await db.update_file_message_id(file_uuid, msg.id, callback.message.chat.id)
                
                if file_data.get("auto_delete"):
                    delete_time = file_data.get("auto_delete_time")
                    if delete_time:
                        info_msg = await msg.reply_text(
                            f"⏳ File Auto-Delete Information\n\n"
                            f"This file will be automatically deleted in {delete_time} minutes\n"
                            f"• Delete Time: {delete_time} minutes\n"
                            f"• Time Left: {delete_time} minutes\n"
                            f"💡 Save this file to your saved messages before it's deleted!",
                            protect_content=config.PRIVACY_MODE
                        )

                        file_link = f"https://t.me/{config.BOT_USERNAME}?start={file_uuid}"
                        asyncio.create_task(schedule_message_deletion(
                            client,
                            callback.message.chat.id,
                            [msg.id, info_msg.id],
                            delete_time,
                            file_link
                        ))
                
                await status_msg.delete()
                
            except Exception as e:
                logger.error(f"Download error: {str(e)}")
                await callback.answer(f"Error: {str(e)}", show_alert=True)
        
        elif callback.data.startswith("share_"):
            file_uuid = callback.data.split("_")[1]
            share_link = f"https://t.me/{config.BOT_USERNAME}?start={file_uuid}"
            await callback.answer(
                f"Share Link: {share_link}",
                show_alert=True
            )
        
        elif callback.data.startswith("dlbatch_"):
            if not await button_manager.check_force_sub(client, callback.from_user.id):
                await callback.answer(
                    "Please join our channel to download files!",
                    show_alert=True
                )
                return
                
            batch_uuid = callback.data.split("_")[1]
            batch_data = await db.get_batch(batch_uuid)
            
            if not batch_data:
                await callback.answer("Batch not found!", show_alert=True)
                return
            
            status_msg = await callback.message.reply_text(
                "🔄 Processing Batch Download\n\n⏳ Please wait..."
            )
            
            success_count = 0
            failed_count = 0
            sent_msgs = []
            delete_time = batch_data.get("auto_delete_time", getattr(config, "DEFAULT_AUTO_DELETE", 30))
            
            for file_uuid in batch_data["files"]:
                file_data = await db.get_file(file_uuid)
                if file_data and "message_id" in file_data:
                    try:
                        msg = await client.copy_message(
                            chat_id=callback.message.chat.id,
                            from_chat_id=config.DB_CHANNEL_ID,
                            message_id=file_data["message_id"],
                            protect_content=config.PRIVACY_MODE
                        )
                        sent_msgs.append(msg.id)
                        success_count += 1
                    except Exception as e:
                        failed_count += 1
                        logger.error(f"Batch download error: {str(e)}")
                        continue
            
            if success_count > 0:
                await db.increment_batch_downloads(batch_uuid)
                
                if batch_data.get("auto_delete", True):
                    info_msg = await status_msg.edit_text(
                        f"✅ Batch Download Complete\n\n"
                        f"📥 Successfully sent: {success_count} files\n"
                        f"❌ Failed: {failed_count} files\n\n"
                        f"⏳ Files will be deleted in {delete_time} minutes"
                    )
                    batch_link = f"https://t.me/{config.BOT_USERNAME}?start=batch_{batch_uuid}"
                    sent_msgs.append(info_msg.id)
                    asyncio.create_task(schedule_message_deletion(
                        client,
                        callback.message.chat.id,
                        sent_msgs,
                        delete_time,
                        batch_link
                    ))
                else:
                    await status_msg.edit_text(
                        f"✅ Batch Download Complete\n\n"
                        f"📥 Successfully sent: {success_count} files\n"
                        f"❌ Failed: {failed_count} files"
                    )
        
        elif callback.data.startswith("share_batch_"):
            batch_uuid = callback.data.split("_")[2]
            share_link = f"https://t.me/{config.BOT_USERNAME}?start=batch_{batch_uuid}"
            await callback.answer(
                f"Share Link: {share_link}",
                show_alert=True
            )
        
        try:
            if not callback.answered:
                await callback.answer()
        except:
            pass
            
    except Exception as e:
        logger.error(f"Callback error: {str(e)}")
        try:
            if not callback.answered:
                await callback.answer("❌ An error occurred", show_alert=True)
        except:
            pass
