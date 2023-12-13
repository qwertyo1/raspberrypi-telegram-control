from gpiozero import GPIOZeroError, CPUTemperature
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

cpu_temperature = None
try:
    cpu_temperature = CPUTemperature()
except GPIOZeroError:
    print("Unable to detect temperature sensor. Are you running the bot on Raspberry Pi?")


async def on_cpu_temp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        f"{cpu_temperature.temperature}C"
        if cpu_temperature is not None and cpu_temperature.temperature
        else "Unable to get CPU temperature"
    )
    await context.bot.sendMessage(chat_id=update.effective_chat.id, text=text)


handlers = [CommandHandler("cputemp", on_cpu_temp)]
