from pyrogram import Client, filters
from pyrogram.types import Message
from handlers.admin.manage_admin import get_all_admin_ids

@Client.on_message(filters.command("auto_del"))
async def auto_delete_command(client: Client, message: Message):
    user_id = message.from_user.id

    admins = await get_all_admin_ids()

    if user_id not in admins:
        return await message.reply_text("__You are not authorized to use this command!__")

    await message.reply_text(
        "**⚙️ Auto Delete Time Configuration Moved**\n\n"
        "The auto-delete feature has been shifted to the `config.py` file.\n"
        "Please open your `config.py` and set the value for `AUTO_DELETE_TIME` there.\n\n"
        "**Example:**\n"
        "`AUTO_DELETE_TIME = 30  # in minutes`\n\n"
        "Restart the bot after updating the configuration to apply changes."
    )
