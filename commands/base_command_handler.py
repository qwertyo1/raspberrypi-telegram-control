from abc import ABC, abstractmethod
from typing import List

from telegram import BotCommand
from telegram.ext import BaseHandler


class BaseCommandHandler(ABC):
    @abstractmethod
    def get_handlers(self) -> List[BaseHandler]:
        pass

    @abstractmethod
    def get_commands(self) -> List[BotCommand]:
        pass
