# © @TheAlphaBotz [2021-2025]
import asyncio, re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import FloodWait, UserIsBlocked, ChatWriteForbidden
from database import Database
from handlers.admin.manage_admin import get_all_admin_ids

db = Database()

broadcast_settings = {"bcast_time": False}

async def load_broadcast_settings():
    broadcast_settings["bcast_time"] = await db.get_setting("bcast_time", False)

async def save_broadcast_setting(key, value):
    broadcast_settings[key] = value
    await db.set_setting(key, value)

@Client.on_message(filters.command("bcast_time") & filters.private)
async def bcast_time(client, message):
    from_user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if from_user_id not in admins:
        return await message.reply_text("__You are not authorized to use this command!__")
    
    cmd = message.text.strip().split(maxsplit=1)
    if len(cmd) != 2 or cmd[1].lower() not in ["on", "off"]:
        return await message.reply("Usage: `/bcast_time on` or `/bcast_time off`")
    status = cmd[1].lower() == "on"
    await save_broadcast_setting("bcast_time", status)
    return await message.reply(f"✅ Timed broadcast is now **{'enabled' if status else 'disabled'}**")

def chunk_buttons(buttons, row_size=4):
    return [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]

def parse_buttons(text):
    if not text:
        return "", None
    pattern = r'\{([^\}]+)\}<url:"(https?://[^"]+)">'
    matches = re.findall(pattern, text)
    buttons = [InlineKeyboardButton(text=btn.strip(), url=url.strip()) for btn, url in matches]
    cleaned = re.sub(pattern, '', text).strip()
    markup = InlineKeyboardMarkup(chunk_buttons(buttons)) if buttons else None
    return cleaned, markup

async def send_broadcast_message(client, user_id, message_to_forward=None, text=None, buttons=None):
    """Helper function to send broadcast message with error handling"""
    try:
        if message_to_forward:
            msg = await message_to_forward.forward(
                chat_id=user_id,
                disable_notification=True
            )
        else:
            msg = await client.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=buttons,
                disable_notification=True
            )
        return True
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_broadcast_message(client, user_id, message_to_forward, text, buttons)
    except (UserIsBlocked, ChatWriteForbidden):
        return False
    except Exception as e:
        print(f"Error broadcasting to {user_id}: {str(e)}")
        return False

@Client.on_message(filters.command("bcast") & filters.private)
async def broadcast_command(client, message: Message):
    from_user_id = message.from_user.id
    admins = await get_all_admin_ids()

    if from_user_id not in admins:
        return await message.reply_text("__You are not authorized to use this command!__")


    delay_hours = 0
    should_pin = False
    message_to_forward = None
    text = None
    buttons = None

    
    if message.reply_to_message:
        message_to_forward = message.reply_to_message
    else:
        if len(message.command) < 2:
            return await message.reply(
                "**Usage:**\n"
                "1. Reply to any message with `/bcast` to forward it\n"
                "2. `/bcast Hello [interval] [pin]` to send text message\n"
                "**Example:** `/bcast Hello 4h pin` = send every 4 hours and pin\n"
                "[Generate buttons](https://alphasharebtngen.netlify.app)"
            )
        content = message.text.split(None, 1)[1]
        words = content.strip().split()
        
    
        if "pin" in words:
            should_pin = True
            words.remove("pin")
        match = re.search(r"(\d+)([hm])$", words[-1]) if words else None
        if match and broadcast_settings["bcast_time"]:
            value, unit = int(match.group(1)), match.group(2)
            delay_hours = value if unit == "h" else value / 60
            words = words[:-1]
        content = " ".join(words)
        text, buttons = parse_buttons(content)

    async def broadcast():
        users = await db.get_all_users()
        total_users = len(users)
        sent, failed = 0, 0
        start_time = asyncio.get_event_loop().time()
        
        status_msg = await message.reply(
            "📣 **Broadcast Started**\n\n"
            f"Total Users: {total_users}\n"
            "Progress: 0%"
        )
        
        update_interval = max(1, total_users // 20)  
        last_update_time = start_time
        
        for i, user in enumerate(users, 1):
            success = await send_broadcast_message(
                client, 
                user["user_id"], 
                message_to_forward,
                text, 
                buttons
            )
            
            if success:
                sent += 1
                if should_pin and message_to_forward:
                    try:
                        await client.pin_chat_message(
                            user["user_id"], 
                            message_to_forward.id, 
                            disable_notification=True
                        )
                    except:
                        pass
            else:
                failed += 1

            
            current_time = asyncio.get_event_loop().time()
            if i % update_interval == 0 or i == total_users:
                if current_time - last_update_time >= 2:  
                    progress = (i / total_users) * 100
                    elapsed_time = current_time - start_time
                    speed = i / elapsed_time if elapsed_time > 0 else 0
                    
                    await status_msg.edit(
                        "📣 **Broadcasting...**\n\n"
                        f"**Total Users:** {total_users}\n"
                        f"**Progress:** {progress:.1f}%\n"
                        f"**Success:** {sent}\n"
                        f"**Failed:** {failed}\n"
                        f"**Speed:** {speed:.1f} messages/sec"
                    )
                    last_update_time = current_time

            
            if i % 100 == 0:
                await asyncio.sleep(0.5)

        time_taken = asyncio.get_event_loop().time() - start_time
        await status_msg.edit(
            "✅ **Broadcast Completed!**\n\n"
            f"**Total Users:** {total_users}\n"
            f"**Successfully Sent:** {sent}\n"
            f"**Failed:** {failed}\n"
            f"**Time Taken:** {time_taken:.1f} seconds\n"
            f"**Average Speed:** {sent/time_taken:.1f} messages/sec"
        )

    if delay_hours > 0:
        while True:
            await broadcast()
            await asyncio.sleep(delay_hours * 3600)
    else:
        await broadcast()
