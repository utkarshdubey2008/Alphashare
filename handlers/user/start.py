# Copyright (c) 2021-2025 @thealphabotz - All Rights Reserved.

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import Database
from utils import ButtonManager
import config
import asyncio
import logging
import base64
from ..utils.message_delete import schedule_message_deletion

logger = logging.getLogger(__name__)
db = Database()
button_manager = ButtonManager()

async def decode_codex_link(encoded_string: str) -> tuple:
    try:
        padding_needed = len(encoded_string) % 4
        if padding_needed:
            encoded_string += '=' * (4 - padding_needed)

        try:
            string_bytes = base64.b64decode(encoded_string.encode("ascii"))
        except Exception:
            encoded_string += '=' * (4 - (len(encoded_string) % 4))
            string_bytes = base64.b64decode(encoded_string.encode("ascii"))

        decoded = string_bytes.decode("ascii")
        if decoded.startswith("get-"):
            parts = decoded.split("-")
            if len(parts) == 2:
                msg_id = int(parts[1]) // abs(config.DB_CHANNEL_ID)
                return False, [msg_id]
            elif len(parts) == 3:
                first_id = int(parts[1]) // abs(config.DB_CHANNEL_ID)
                last_id = int(parts[2]) // abs(config.DB_CHANNEL_ID)
                return True, list(range(first_id, last_id + 1))
        return False, []
    except Exception as e:
        logger.error(f"Error decoding CodeXBotz link: {str(e)}")
        return False, []

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    try:
        await db.add_user(message.from_user.id, message.from_user.mention)
    except Exception as e:
        logger.error(f"Error adding user to database: {str(e)}")

    user_method = message.from_user.mention if message.from_user.mention else message.from_user.first_name

    if len(message.command) > 1:
        command = message.command[1]

        force_sub_status = await button_manager.check_force_sub(client, message.from_user.id)
        if not force_sub_status:
            force_sub_text = "**⚠️ You must join our channel(s) to use this bot!**\n\n"
            channels = [
                (config.FORCE_SUB_CHANNEL, "Join Channel 1"),
                (config.FORCE_SUB_CHANNEL_2, "Join Channel 2"),
                (config.FORCE_SUB_CHANNEL_3, "Join Channel 3"),
                (config.FORCE_SUB_CHANNEL_4, "Join Channel 4")
            ]

            for ch_id, name in channels:
                if ch_id != 0:
                    force_sub_text += f"• Join {name}\n"

            force_sub_text += "\nJoin the channel(s) and try again."

            await message.reply_text(
                force_sub_text,
                reply_markup=button_manager.force_sub_button(),
                protect_content=config.PRIVACY_MODE
            )
            return

        is_codex_batch, message_ids = await decode_codex_link(command)

        if message_ids:
            if is_codex_batch:
                status_msg = await message.reply_text(
                    f"🔄 **Processing Batch Download**\n\n"
                    f"📦 Total Files: {len(message_ids)}\n"
                    f"⏳ Please wait...",
                    protect_content=config.PRIVACY_MODE
                )

                success_count = 0
                failed_count = 0
                sent_msgs = []

                for msg_id in message_ids:
                    try:
                        msg = await client.copy_message(
                            chat_id=message.chat.id,
                            from_chat_id=config.DB_CHANNEL_ID,
                            message_id=msg_id,
                            protect_content=config.PRIVACY_MODE
                        )
                        if msg:
                            sent_msgs.append(msg.id)
                            success_count += 1
                    except Exception as e:
                        failed_count += 1
                        logger.error(f"Batch file send error: {str(e)}")
                        continue

                if success_count > 0 and config.AUTO_DELETE_TIME:
                    delete_time = config.AUTO_DELETE_TIME
                    info_msg = await client.send_message(
                        chat_id=message.chat.id,
                        text=f"⏳ **Auto Delete Information**\n\n"
                             f"➜ This file will be deleted in {delete_time} minutes.\n"
                             f"➜ Forward this file to your saved messages or another chat to save it permanently.",
                        protect_content=config.PRIVACY_MODE
                    )
                    if info_msg and info_msg.id:
                        sent_msgs.append(info_msg.id)
                        asyncio.create_task(schedule_message_deletion(
                            client, message.chat.id, sent_msgs, delete_time
                        ))

                status_text = (
                    f"✅ **Batch Download Complete**\n\n"
                    f"📥 Successfully sent: {success_count} files\n"
                    f"❌ Failed: {failed_count} files"
                )
                await status_msg.edit_text(status_text)
                return

            else:
                try:
                    msg = await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=config.DB_CHANNEL_ID,
                        message_id=message_ids[0],
                        protect_content=config.PRIVACY_MODE
                    )
                    if msg:
                        if config.AUTO_DELETE_TIME:
                            delete_time = config.AUTO_DELETE_TIME
                            info_msg = await msg.reply_text(
                                f"⏳ **Auto Delete Information**\n\n"
                                f"➜ This file will be deleted in {delete_time} minutes.\n"
                                f"➜ Forward this file to your saved messages or another chat to save it permanently.",
                                protect_content=config.PRIVACY_MODE
                            )
                            if info_msg and info_msg.id:
                                asyncio.create_task(schedule_message_deletion(
                                    client, message.chat.id, [msg.id, info_msg.id], delete_time
                                ))
                    return
                except Exception as e:
                    await message.reply_text(
                        "❌ File not found or has been deleted!",
                        protect_content=config.PRIVACY_MODE
                    )
                    return

        if command.startswith("batch_"):
            batch_uuid = command.replace("batch_", "")
            batch_data = await db.get_batch(batch_uuid)

            if not batch_data:
                await message.reply_text(
                    "❌ Batch not found or has been deleted!",
                    protect_content=config.PRIVACY_MODE
                )
                return

            status_msg = await message.reply_text(
                f"🔄 **Processing Batch Download**\n\n"
                f"📦 Total Files: {len(batch_data['files'])}\n"
                f"⏳ Please wait...",
                protect_content=config.PRIVACY_MODE
            )

            success_count = 0
            failed_count = 0
            sent_msgs = []

            for file_uuid in batch_data["files"]:
                file_data = await db.get_file(file_uuid)
                if file_data and "message_id" in file_data:
                    try:
                        msg = await client.copy_message(
                            chat_id=message.chat.id,
                            from_chat_id=config.DB_CHANNEL_ID,
                            message_id=file_data["message_id"],
                            protect_content=config.PRIVACY_MODE
                        )
                        if msg and msg.id:
                            sent_msgs.append(msg.id)
                            success_count += 1
                    except Exception as e:
                        failed_count += 1
                        logger.error(f"Batch file send error: {str(e)}")
                        continue

            if success_count > 0 and config.AUTO_DELETE_TIME:
                delete_time = config.AUTO_DELETE_TIME
                info_msg = await client.send_message(
                    chat_id=message.chat.id,
                    text=f"⏳ **Auto Delete Information**\n\n"
                         f"➜ This file will be deleted in {delete_time} minutes.\n"
                         f"➜ Forward this file to your saved messages or another chat to save it permanently.",
                    protect_content=config.PRIVACY_MODE
                )
                if info_msg and info_msg.id:
                    sent_msgs.append(info_msg.id)
                    asyncio.create_task(schedule_message_deletion(
                        client, message.chat.id, sent_msgs, delete_time
                    ))

            if success_count > 0:
                await db.increment_batch_downloads(batch_uuid)

            status_text = (
                f"✅ **Batch Download Complete**\n\n"
                f"📥 Successfully sent: {success_count} files\n"
                f"❌ Failed: {failed_count} files"
            )
            await status_msg.edit_text(status_text)

        else:
            file_uuid = command
            file_data = await db.get_file(file_uuid)

            if not file_data:
                await message.reply_text(
                    "❌ File not found or has been deleted!",
                    protect_content=config.PRIVACY_MODE
                )
                return

            try:
                msg = await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=config.DB_CHANNEL_ID,
                    message_id=file_data["message_id"],
                    protect_content=config.PRIVACY_MODE
                )

                if msg and msg.id:
                    await db.increment_downloads(file_uuid)

                    if config.AUTO_DELETE_TIME:
                        delete_time = config.AUTO_DELETE_TIME
                        info_msg = await msg.reply_text(
                            f"⏳ **Auto Delete Information**\n\n"
                            f"➜ This file will be deleted in {delete_time} minutes.\n"
                            f"➜ Forward this file to your saved messages or another chat to save it permanently.",
                            protect_content=config.PRIVACY_MODE
                        )
                        if info_msg and info_msg.id:
                            asyncio.create_task(schedule_message_deletion(
                                client, message.chat.id, [msg.id, info_msg.id], delete_time
                            ))

            except Exception as e:
                await message.reply_text(
                    f"❌ Error: {str(e)}",
                    protect_content=config.PRIVACY_MODE
                )

    else:
        buttons = button_manager.start_button()
        await message.reply_photo(
            photo=config.START_PHOTO, 
            caption=config.Messages.START_TEXT.format(
                bot_name=config.BOT_NAME,
                user_mention=user_method
            ),
            reply_markup=buttons
                    )
