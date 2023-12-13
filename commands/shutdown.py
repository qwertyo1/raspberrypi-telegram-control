import subprocess

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler


async def _on_shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton(text="Confirm", callback_data="confirm_shutdown")]]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.sendMessage(
        chat_id=update.effective_chat.id,
        text="Please confirm shutdown command sending",
        reply_markup=markup,
    )


async def _on_confirm_shutdown_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.sendMessage(chat_id=update.effective_chat.id, text="Shutting down...")
    subprocess.call("sudo shutdown -h now", shell=True)
    await update.callback_query.answer()


handlers = [
    CommandHandler("shutdown", _on_shutdown),
    CallbackQueryHandler(_on_confirm_shutdown_button, "confirm_shutdown"),
]
