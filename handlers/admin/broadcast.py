import asyncio, re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from database import Database
from utils import is_admin

db = Database()

broadcast_settings = {"bcast_time": False}

async def load_broadcast_settings():
    broadcast_settings["bcast_time"] = await db.get_setting("bcast_time", False)

async def save_broadcast_setting(key, value):
    broadcast_settings[key] = value
    await db.set_setting(key, value)

@Client.on_message(filters.command("bcast_time") & filters.private)
async def bcast_time(client, message):
    if not is_admin(message):
        return await message.reply("⚠️ You are not authorized to use this command!")
    cmd = message.text.strip().split(maxsplit=1)
    if len(cmd) != 2 or cmd[1].lower() not in ["on", "off"]:
        return await message.reply("Usage: `/bcast_time on` or `/bcast_time off`")
    status = cmd[1].lower() == "on"
    await save_broadcast_setting("bcast_time", status)
    return await message.reply(f"✅ Timed broadcast is now **{'enabled' if status else 'disabled'}**")

def chunk_buttons(buttons, row_size=4):
    return [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]

def parse_buttons(text):
    pattern = r'\{([^\}]+)\}<url:"(https?://[^"]+)">'
    matches = re.findall(pattern, text)
    buttons = [InlineKeyboardButton(text=btn.strip(), url=url.strip()) for btn, url in matches]
    cleaned = re.sub(pattern, '', text).strip()
    markup = InlineKeyboardMarkup(chunk_buttons(buttons)) if buttons else None
    return cleaned, markup

@Client.on_message(filters.command("bcast") & filters.private)
async def broadcast_command(client, message: Message):
    if not is_admin(message):
        return await message.reply("⚠️ You are not authorized to use this command!")

    users = await db.get_all_users()
    text, media, caption, buttons = None, None, None, None
    delay_hours, should_pin = 0, False

    if message.reply_to_message:
        media = (
            message.reply_to_message.photo or
            message.reply_to_message.video or
            message.reply_to_message.document or
            message.reply_to_message.audio or
            message.reply_to_message.animation
        )
        caption, buttons = parse_buttons(message.reply_to_message.caption or message.reply_to_message.text or "")
    else:
        if len(message.command) < 2:
            return await message.reply(
                "**Usage:** `/bcast Hello [interval] [pin]`\n"
                "**Example:** `/bcast Hello 4h pin` = send every 4 hours and pin the message\n"
                "Or reply to a media/text with `/bcast`\n"
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
        sent, failed = 0, 0
        status_msg = await message.reply("📣 Broadcasting started...\nSending to users...")
        for i, user in enumerate(users):
            try:
                if media:
                    msg = await client.send_photo(
                        chat_id=user["user_id"],
                        photo=media.file_id,
                        caption=caption,
                        reply_markup=buttons
                    )
                else:
                    msg = await client.send_message(
                        chat_id=user["user_id"],
                        text=text,
                        reply_markup=buttons
                    )
                if should_pin:
                    try:
                        await client.pin_chat_message(user["user_id"], msg.id, disable_notification=True)
                    except:
                        pass
                sent += 1
            except:
                failed += 1
            if i % 20 == 0:
                await asyncio.sleep(1)
        await status_msg.edit(f"✅ Broadcast complete!\n\n**Sent:** {sent}\n**Failed:** {failed}")

    if delay_hours > 0:
        while True:
            await broadcast()
            await asyncio.sleep(delay_hours * 3600)
    else:
        await broadcast()
