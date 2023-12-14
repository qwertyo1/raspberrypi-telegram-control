import datetime

from telegram.ext import ApplicationBuilder, Application

from commands.reboot import RebootCommandHandler
from commands.shutdown import ShutdownCommandHandler
from commands.temperature import TemperatureCommandHandler
from settings import settings

now = datetime.datetime.now()

handlers = [RebootCommandHandler(), ShutdownCommandHandler(), TemperatureCommandHandler()]


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [command for handler in handlers for command in handler.get_commands()]
    )
    print(await application.bot.getMe())


if __name__ == "__main__":
    application = ApplicationBuilder().token(settings.bot_token).post_init(post_init).build()

    application.add_handlers(
        [command_handler for handler in handlers for command_handler in handler.get_handlers()]
    )

    application.run_polling()
