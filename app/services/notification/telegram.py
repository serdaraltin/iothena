from typing import Dict

from app.models.notification.telegram import TelegramModel
from app.services.systems.config import CONFIG
from app.services.systems.logger import LOGGER


class TelegramService:

    def __repr__(self):
        return repr(self.__dict__)

    def __init__(self):
        self.cls_name = self.__class__.__name__
        self.config = CONFIG.notification['settings']['telegram']
        self.bots = None

    def get_bots(self) -> Dict[str, TelegramModel]:
        return {
            bot["name"]: bot
            for bot in self.config["bots"]
        }

    def get_bot(self, bot_name):
        return self.get_bots()[bot_name]

    def initialize(self, message="Initialized"):
        self.bots = self.get_bots()

        for name,bot in self.get_bots().items():
            try:
                bot.send_message(message)
                LOGGER.info(f"[{self.cls_name}] Telegram bot initialized: Bot={name}")
            except Exception as e:
                LOGGER.error(f"[{self.cls_name}] Bot initialize message failed: {e}")

        LOGGER.info(f"[{self.cls_name}] Telegram bot initialized")

    def update(self):
        self.bots = self.get_bots()
        self.initialize(message="Updated")
        LOGGER.info(f"[{self.cls_name}] Telegram bot updated")

    def start(self):
        self.initialize()



TELEGRAM_SERVICE = TelegramService()