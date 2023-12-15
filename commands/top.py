import subprocess
import textwrap
from prettytable import PrettyTable, MARKDOWN
from typing import List

from telegram import BotCommand, Update
from telegram.ext import BaseHandler, ContextTypes, CommandHandler

from commands.base_command_handler import BaseCommandHandler


async def _on_top(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = subprocess.Popen("top -n1 -bci", shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    text = ""
    table = PrettyTable(max_table_width=46, min_table_width=46, align="l")
    table.set_style(MARKDOWN)
    table.left_padding_width = 0
    table.right_padding_width = 0
    table.field_names = ["PID", "USER", "%CPU", "%MEM", "CMD"]
    line_number = 0
    for line in result.stdout.readlines():
        if line_number < 6:
            line_number += 1
            text += line
            continue
        if line_number == 6:
            line_number += 1
            continue
        pid, user, pr, ni, virt, res, shr, s, cpu, mem, time, *command = line.split()
        table.add_row([pid, user, cpu, mem, textwrap.fill(" ".join(command), 20)])
        line_number += 1
    text += "```\n" + table.get_string() + "\n```"
    print(text)
    await context.bot.sendMessage(
        chat_id=update.effective_chat.id, text=text, parse_mode="Markdown"
    )


class TopCommandHandler(BaseCommandHandler):
    command = "top"

    def get_commands(self) -> List[BotCommand]:
        return [BotCommand(self.command, "Show output of top command")]

    def get_handlers(self) -> List[BaseHandler]:
        return [CommandHandler(self.command, _on_top)]
