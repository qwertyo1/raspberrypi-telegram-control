import subprocess
from typing import List

from telegram import Update, BotCommand
from telegram.ext import ContextTypes, CommandHandler, BaseHandler

from commands.base_command_handler import BaseCommandHandler


async def _on_reboot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.sendMessage(chat_id=update.effective_chat.id, text="Rebooting...")
    subprocess.call("sudo reboot", shell=True)


class RebootCommandHandler(BaseCommandHandler):
    command = "reboot"

    def get_commands(self) -> List[BotCommand]:
        return [BotCommand(self.command, "Reboot")]

    def get_handlers(self) -> List[BaseHandler]:
        return [CommandHandler(self.command, _on_reboot)]
