import datetime

from telegram.ext import ApplicationBuilder, Application

from commands.reboot import handlers as reboot_handlers
from commands.shutdown import handlers as shutdown_handlers
from commands.temperature import handlers as temperature_handlers
from settings import settings

now = datetime.datetime.now()


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [("cputemp", "CPU temperature"), ("reboot", "Reboot"), ("shutdown", "Shutdown")]
    )
    print(await application.bot.getMe())


if __name__ == "__main__":
    application = ApplicationBuilder().token(settings.bot_token).post_init(post_init).build()

    application.add_handlers([*reboot_handlers, *shutdown_handlers, *temperature_handlers])

    application.run_polling()
