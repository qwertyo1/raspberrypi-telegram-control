from typing import List

from gpiozero import GPIOZeroError, CPUTemperature
from telegram import Update, BotCommand
from telegram.ext import CommandHandler, ContextTypes, BaseHandler

from commands.base_command_handler import BaseCommandHandler

cpu_temperature = None
try:
    cpu_temperature = CPUTemperature()
except GPIOZeroError:
    print("Unable to detect temperature sensor. Are you running the bot on Raspberry Pi?")


async def _on_cpu_temp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        f"{cpu_temperature.temperature}C"
        if cpu_temperature is not None and cpu_temperature.temperature
        else "Unable to get CPU temperature"
    )
    await context.bot.sendMessage(chat_id=update.effective_chat.id, text=text)


class TemperatureCommandHandler(BaseCommandHandler):
    command = "cputemp"

    def get_commands(self) -> List[BotCommand]:
        if cpu_temperature is None:
            return []
        return [BotCommand(self.command, "CPU temperature")]

    def get_handlers(self) -> List[BaseHandler]:
        if cpu_temperature is None:
            return []
        return [CommandHandler("cputemp", _on_cpu_temp)]
