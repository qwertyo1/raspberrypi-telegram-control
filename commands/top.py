import subprocess
import textwrap
from prettytable import PrettyTable, MARKDOWN
from typing import List

from telegram import BotCommand, Update
from telegram.ext import BaseHandler, ContextTypes, CommandHandler

from commands.base_command_handler import BaseCommandHandler


def _handle_top_line(line: str) -> str:
    time = f"Time: {line[6:14]}."

    def get_uptime() -> str:
        raw_uptime = line[15:].split(",").pop(0)
        uptime_start = -1
        for i, c in enumerate(raw_uptime):
            if c.isdigit():
                uptime_start = i
                break
        if uptime_start < 0:
            return ""
        return f"Uptime: {raw_uptime[uptime_start:]}."

    uptime = get_uptime()
    return " ".join([time, uptime]) + "\n"


line_handlers = {0: _handle_top_line, 6: lambda line: ""}


async def _on_top(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = subprocess.Popen(
        "top -n1 -bci -w 512", shell=True, stdout=subprocess.PIPE, encoding="utf-8"
    )
    text = "```\n"
    table = PrettyTable(max_table_width=46, min_table_width=46, align="l")
    table.set_style(MARKDOWN)
    table.left_padding_width = 0
    table.right_padding_width = 0
    table.field_names = ["PID", "USER", "%CPU", "%MEM", "CMD"]
    line_number = 0
    for line in result.stdout.readlines():
        if line_number < 7:
            line_handler = line_handlers.get(line_number)
            text += line_handler(line) if line_handler is not None else line
            line_number += 1
            continue
        pid, user, pr, ni, virt, res, shr, s, cpu, mem, time, *command = line.split()
        table.add_row([pid, user, cpu, mem, textwrap.fill(" ".join(command), 19)])
        line_number += 1
    text += table.get_string() + "\n```"
    await context.bot.sendMessage(
        chat_id=update.effective_chat.id, text=text, parse_mode="Markdown"
    )


class TopCommandHandler(BaseCommandHandler):
    command = "top"

    def get_commands(self) -> List[BotCommand]:
        return [BotCommand(self.command, "Show output of top command")]

    def get_handlers(self) -> List[BaseHandler]:
        return [CommandHandler(self.command, _on_top)]
