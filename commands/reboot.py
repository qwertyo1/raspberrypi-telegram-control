import subprocess

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def _on_reboot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.sendMessage(chat_id=update.effective_chat.id, text="Rebooting...")
    subprocess.call("sudo reboot", shell=True)


handlers = [CommandHandler("reboot", _on_reboot)]
