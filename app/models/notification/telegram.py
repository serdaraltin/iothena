from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from app.models.base import BaseModel

class TelegramModel(BaseModel):

    def __repr__(self):
        return repr(self.__dict__)

    def __init__(self, bot_token: str, chat_id: int):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_message(self, message: str):
        pass
