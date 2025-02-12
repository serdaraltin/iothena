import threading
import time
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
        self.bots = {}
        self._thread = None
        self._stop_event = threading.Event()

    def get_bots(self) -> Dict[str, TelegramModel]:
        """Returns the list of Telegram bots."""
        return {bot["name"]: bot for bot in self.config["bots"]}

    def get_bot(self, bot_name):
        """Gets a specific Telegram bot by name."""
        return self.get_bots().get(bot_name)

    def initialize(self, message="Initialized"):
        """Initializes all Telegram bots and sends a message."""
        self.bots = self.get_bots()

        for name, bot in self.bots.items():
            try:
                bot.send_message(message)
                LOGGER.info(f"Telegram bot initialized: Bot={name}")
            except Exception as e:
                LOGGER.error(f"Bot initialize message failed: {e}")

        LOGGER.info(f"Telegram bot initialized")

    def update(self):
        """Updates bot configurations and re-initializes."""
        self.bots = self.get_bots()
        self.initialize(message="Updated")
        LOGGER.info(f"Telegram bot updated")

    def run(self, stop_event):
        """Main loop to keep the service running."""
        LOGGER.info("Starting Telegram Service...")
        self.initialize()
        while not stop_event.is_set():
            time.sleep(10)  # Adjust sleep time as needed

        LOGGER.info(f"Stopping Telegram service...")

    def start(self):
        """Starts the TelegramService in a separate thread."""
        if self._thread and self._thread.is_alive():
            LOGGER.warning(f"Telegram service is already running.")
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self.run, args=(self._stop_event,), daemon=True)
        self._thread.start()
        LOGGER.info(f"Telegram service started.")

    def stop(self):
        """Stops the TelegramService."""
        if not self._thread or not self._thread.is_alive():
            LOGGER.warning(f"Telegram service is not running.")
            return

        LOGGER.info(f"Stopping Telegram service...")
        self._stop_event.set()
        self._thread.join()
        LOGGER.info(f"Telegram service stopped.")


TELEGRAM_SERVICE = TelegramService()
