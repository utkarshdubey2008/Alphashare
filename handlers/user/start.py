# -*- coding: utf-8 -*-
# Copyright (c) 2021-2025 @thealphabotz - All Rights Reserved.

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
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

active_batch_users = set()

class Emoji:
    WARNING = "\u26A0\uFE0F"
    SUCCESS = "\u2705"
    ERROR = "\u274C"
    LOADING = "\U0001F504"
    BOX = "\U0001F4E6"
    HOURGLASS = "\u231B"
    INBOX = "\U0001F4E5"
    ARROW = "\u279C"
    BULLET = "\u2022"

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

async def send_batch_files(client: Client, message: Message, message_ids: list, is_codex: bool = False):
    user_id = message.from_user.id
    
    if user_id in active_batch_users:
        await message.reply_text(
            f"{Emoji.WARNING} **Pʟᴇᴀꜱᴇ Wᴀɪᴛ!**\n\n"
            f"Yᴏᴜ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴀɴ ᴏɴɢᴏɪɴɢ ʙᴀᴛᴄʜ ᴘʀᴏᴄᴇꜱꜱ.\n"
            f"Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ ꜰᴏʀ ɪᴛ ᴛᴏ ᴄᴏᴍᴘʟᴇᴛᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.",
            protect_content=config.PRIVACY_MODE
        )
        return
    
    active_batch_users.add(user_id)
    
    try:
        status_msg = await message.reply_text(
            f"{Emoji.LOADING} **Pʀᴏᴄᴇꜱꜱɪɴɢ...**",
            protect_content=config.PRIVACY_MODE
        )
        
        success_count = 0
        failed_count = 0
        sent_msgs = []
        first_file_sent = False
        
        for idx, msg_id in enumerate(message_ids, 1):
            try:
                max_retries = 3
                retry_count = 0
                
                while retry_count < max_retries:
                    try:
                        msg = await client.copy_message(
                            chat_id=message.chat.id,
                            from_chat_id=config.DB_CHANNEL_ID,
                            message_id=msg_id,
                            protect_content=config.PRIVACY_MODE
                        )
                        
                        if msg and msg.id:
                            sent_msgs.append(msg.id)
                            success_count += 1
                            
                            if not first_file_sent:
                                try:
                                    await status_msg.delete()
                                except:
                                    pass
                                first_file_sent = True
                        
                        break
                        
                    except FloodWait as e:
                        wait_time = e.value
                        if first_file_sent:
                            flood_msg = await message.reply_text(
                                f"{Emoji.HOURGLASS} **Fʟᴏᴏᴅᴡᴀɪᴛ {wait_time} ꜱᴇᴄᴏɴᴅꜱ. Rᴇꜱᴜᴍɪɴɢ...**\n\n"
                                f"Sᴇɴᴛ: {success_count}/{len(message_ids)}",
                                protect_content=config.PRIVACY_MODE
                            )
                        else:
                            try:
                                await status_msg.edit_text(
                                    f"{Emoji.HOURGLASS} **Fʟᴏᴏᴅᴡᴀɪᴛ {wait_time} ꜱᴇᴄᴏɴᴅꜱ. Rᴇꜱᴜᴍɪɴɢ...**",
                                    protect_content=config.PRIVACY_MODE
                                )
                            except:
                                pass
                        
                        await asyncio.sleep(wait_time)
                        retry_count += 1
                        
                        if first_file_sent:
                            try:
                                await flood_msg.delete()
                            except:
                                pass
                    
                    except Exception as e:
                        if retry_count >= max_retries - 1:
                            raise
                        await asyncio.sleep(2)
                        retry_count += 1
                
            except Exception as e:
                failed_count += 1
                logger.error(f"Batch file send error: {str(e)}")
                continue
        
        if success_count > 0 and config.AUTO_DELETE_TIME:
            delete_time = config.AUTO_DELETE_TIME
            info_msg = await client.send_message(
                chat_id=message.chat.id,
                text=f"{Emoji.HOURGLASS} **Aᴜᴛᴏ Dᴇʟᴇᴛᴇ Iɴꜰᴏʀᴍᴀᴛɪᴏɴ**\n\n"
                     f"{Emoji.ARROW} Fɪʟᴇꜱ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ {delete_time} ᴍɪɴᴜᴛᴇꜱ.\n"
                     f"{Emoji.ARROW} Fᴏʀᴡᴀʀᴅ ᴛᴏ ꜱᴀᴠᴇ ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ.",
                protect_content=config.PRIVACY_MODE
            )
            if info_msg and info_msg.id:
                sent_msgs.append(info_msg.id)
                asyncio.create_task(schedule_message_deletion(
                    client, message.chat.id, sent_msgs, delete_time
                ))
        
        if not first_file_sent:
            try:
                await status_msg.edit_text(
                    f"{Emoji.ERROR} **Nᴏ Fɪʟᴇꜱ Fᴏᴜɴᴅ**\n\n"
                    f"Aʟʟ ꜰɪʟᴇꜱ ᴍᴀʏ ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ᴏʀ ᴀʀᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ."
                )
            except:
                pass
        elif failed_count > 0:
            summary_msg = await message.reply_text(
                f"{Emoji.SUCCESS} **Sᴇɴᴛ:** {success_count} | {Emoji.ERROR} **Fᴀɪʟᴇᴅ:** {failed_count}",
                protect_content=config.PRIVACY_MODE
            )
    
    finally:
        active_batch_users.discard(user_id)

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    try:
        await db.add_user(message.from_user.id, message.from_user.mention)
    except Exception as e:
        logger.error(f"Error adding user to database: {str(e)}")

    user_method = message.from_user.mention if message.from_user.mention else message.from_user.first_name
    user_mention = message.from_user.mention if message.from_user.mention else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

    if len(message.command) > 1:
        command = message.command[1]
        file_uuid = message.command[1]

        force_sub_status = await button_manager.check_force_sub(client, message.from_user.id)
        if not force_sub_status:
            force_sub_text = f"**{Emoji.WARNING} Yᴏᴜ ᴍᴜꜱᴛ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ(ꜱ) ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ!**\n\n"
            channels = [
                (config.FORCE_SUB_CHANNEL, "Join Channel 1"),
                (config.FORCE_SUB_CHANNEL_2, "Join Channel 2"),
                (config.FORCE_SUB_CHANNEL_3, "Join Channel 3"),
                (config.FORCE_SUB_CHANNEL_4, "Join Channel 4")
            ]

            for ch_id, name in channels:
                if ch_id != 0:
                    force_sub_text += f"{Emoji.BULLET} {name}\n"

            force_sub_text += "\nJᴏɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ(ꜱ) ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ."

            await message.reply_text(
                force_sub_text,
                reply_markup=button_manager.force_sub_button_new(file_uuid),
                protect_content=config.PRIVACY_MODE
            )
            return

        is_codex_batch, message_ids = await decode_codex_link(command)

        if message_ids:
            if is_codex_batch:
                await send_batch_files(client, message, message_ids, is_codex=True)
                return
            else:
                try:
                    msg = await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=config.DB_CHANNEL_ID,
                        message_id=message_ids[0],
                        protect_content=config.PRIVACY_MODE
                    )
                    if msg and msg.id:
                        if config.AUTO_DELETE_TIME:
                            delete_time = config.AUTO_DELETE_TIME
                            info_msg = await msg.reply_text(
                                f"{Emoji.HOURGLASS} **Aᴜᴛᴏ Dᴇʟᴇᴛᴇ Iɴꜰᴏʀᴍᴀᴛɪᴏɴ**\n\n"
                                f"{Emoji.ARROW} Fɪʟᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ {delete_time} ᴍɪɴᴜᴛᴇꜱ.\n"
                                f"{Emoji.ARROW} Fᴏʀᴡᴀʀᴅ ᴛᴏ ꜱᴀᴠᴇ ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ.",
                                protect_content=config.PRIVACY_MODE
                            )
                            if info_msg and info_msg.id:
                                asyncio.create_task(schedule_message_deletion(
                                    client, message.chat.id, [msg.id, info_msg.id], delete_time
                                ))
                    return
                except Exception:
                    await message.reply_text(
                        f"{Emoji.ERROR} Fɪʟᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ ᴏʀ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ!",
                        protect_content=config.PRIVACY_MODE
                    )
                    return

        if command.startswith("batch_"):
            user_id = message.from_user.id
            
            if user_id in active_batch_users:
                await message.reply_text(
                    f"{Emoji.WARNING} **Pʟᴇᴀꜱᴇ Wᴀɪᴛ!**\n\n"
                    f"Yᴏᴜ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴀɴ ᴏɴɢᴏɪɴɢ ʙᴀᴛᴄʜ ᴘʀᴏᴄᴇꜱꜱ.\n"
                    f"Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ ꜰᴏʀ ɪᴛ ᴛᴏ ᴄᴏᴍᴘʟᴇᴛᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.",
                    protect_content=config.PRIVACY_MODE
                )
                return
            
            batch_uuid = command.replace("batch_", "")
            batch_data = await db.get_batch(batch_uuid)

            if not batch_data:
                await message.reply_text(
                    f"{Emoji.ERROR} Bᴀᴛᴄʜ ɴᴏᴛ ꜰᴏᴜɴᴅ ᴏʀ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ!",
                    protect_content=config.PRIVACY_MODE
                )
                return

            active_batch_users.add(user_id)
            
            try:
                status_msg = await message.reply_text(
                    f"{Emoji.LOADING} **Pʀᴏᴄᴇꜱꜱɪɴɢ...**",
                    protect_content=config.PRIVACY_MODE
                )
                
                success_count = 0
                failed_count = 0
                sent_msgs = []
                first_file_sent = False
                total_files = len(batch_data["files"])

                for file_uuid in batch_data["files"]:
                    file_data = await db.get_file(file_uuid)
                    if file_data and "message_id" in file_data:
                        try:
                            max_retries = 3
                            retry_count = 0
                            
                            while retry_count < max_retries:
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
                                        
                                        if not first_file_sent:
                                            try:
                                                await status_msg.delete()
                                            except:
                                                pass
                                            first_file_sent = True
                                    
                                    break
                                    
                                except FloodWait as e:
                                    wait_time = e.value
                                    if first_file_sent:
                                        flood_msg = await message.reply_text(
                                            f"{Emoji.HOURGLASS} **Fʟᴏᴏᴅᴡᴀɪᴛ {wait_time} ꜱᴇᴄᴏɴᴅꜱ. Rᴇꜱᴜᴍɪɴɢ...**\n\n"
                                            f"Sᴇɴᴛ: {success_count}/{total_files}",
                                            protect_content=config.PRIVACY_MODE
                                        )
                                    else:
                                        try:
                                            await status_msg.edit_text(
                                                f"{Emoji.HOURGLASS} **Fʟᴏᴏᴅᴡᴀɪᴛ {wait_time} ꜱᴇᴄᴏɴᴅꜱ. Rᴇꜱᴜᴍɪɴɢ...**",
                                                protect_content=config.PRIVACY_MODE
                                            )
                                        except:
                                            pass
                                    
                                    await asyncio.sleep(wait_time)
                                    retry_count += 1
                                    
                                    if first_file_sent:
                                        try:
                                            await flood_msg.delete()
                                        except:
                                            pass
                                
                                except Exception as e:
                                    if retry_count >= max_retries - 1:
                                        raise
                                    await asyncio.sleep(2)
                                    retry_count += 1
                            
                        except Exception as e:
                            failed_count += 1
                            logger.error(f"Batch file send error: {str(e)}")
                            continue

                if success_count > 0:
                    await db.increment_batch_downloads(batch_uuid)
                    if config.AUTO_DELETE_TIME:
                        delete_time = config.AUTO_DELETE_TIME
                        info_msg = await client.send_message(
                            chat_id=message.chat.id,
                            text=f"{Emoji.HOURGLASS} **Aᴜᴛᴏ Dᴇʟᴇᴛᴇ Iɴꜰᴏʀᴍᴀᴛɪᴏɴ**\n\n"
                                 f"{Emoji.ARROW} Fɪʟᴇꜱ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ {delete_time} ᴍɪɴᴜᴛᴇꜱ.\n"
                                 f"{Emoji.ARROW} Fᴏʀᴡᴀʀᴅ ᴛᴏ ꜱᴀᴠᴇ ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ.",
                            protect_content=config.PRIVACY_MODE
                        )
                        if info_msg and info_msg.id:
                            sent_msgs.append(info_msg.id)
                            asyncio.create_task(schedule_message_deletion(
                                client, message.chat.id, sent_msgs, delete_time
                            ))

                if not first_file_sent:
                    try:
                        await status_msg.edit_text(
                            f"{Emoji.ERROR} **Nᴏ Fɪʟᴇꜱ Fᴏᴜɴᴅ**\n\n"
                            f"Aʟʟ ꜰɪʟᴇꜱ ᴍᴀʏ ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ."
                        )
                    except:
                        pass
                elif failed_count > 0:
                    await message.reply_text(
                        f"{Emoji.SUCCESS} **Sᴇɴᴛ:** {success_count} | {Emoji.ERROR} **Fᴀɪʟᴇᴅ:** {failed_count}",
                        protect_content=config.PRIVACY_MODE
                    )
            
            finally:
                active_batch_users.discard(user_id)

        else:
            file_uuid = command
            file_data = await db.get_file(file_uuid)

            if not file_data:
                await message.reply_text(
                    f"{Emoji.ERROR} Fɪʟᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ ᴏʀ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ!",
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
                            f"{Emoji.HOURGLASS} **Aᴜᴛᴏ Dᴇʟᴇᴛᴇ Iɴꜰᴏʀᴍᴀᴛɪᴏɴ**\n\n"
                            f"{Emoji.ARROW} Fɪʟᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ {delete_time} ᴍɪɴᴜᴛᴇꜱ.\n"
                            f"{Emoji.ARROW} Fᴏʀᴡᴀʀᴅ ᴛᴏ ꜱᴀᴠᴇ ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ.",
                            protect_content=config.PRIVACY_MODE
                        )
                        if info_msg and info_msg.id:
                            asyncio.create_task(schedule_message_deletion(
                                client, message.chat.id, [msg.id, info_msg.id], delete_time
                            ))

            except Exception as e:
                await message.reply_text(
                    f"{Emoji.ERROR} Eʀʀᴏʀ: {str(e)}", 
                    protect_content=config.PRIVACY_MODE
                )

    else:
        buttons = button_manager.start_button()
        await message.reply_photo(
            photo=config.START_PHOTO, 
            caption=config.Messages.START_TEXT.format(
                bot_name=config.BOT_NAME,
                user_method=user_method,
                user_mention=user_mention
            ),
            reply_markup=buttons
                                    )
