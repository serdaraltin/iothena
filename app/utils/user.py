import getpass
import psutil

from app.utils.base import BaseInfo


class User(BaseInfo):

    def __init__(self):
        self.user = self.get_current_user()
        self.all_user = self.get_users()


    @staticmethod
    def get_current_user():
        users = psutil.users()
        for user in users:
            if user.name == getpass.getuser():
                return {
                    'name': user.name,
                    'term': user.terminal,
                    'host': user.host,
                    'started': user.started,
                    'pid': user.pid,
                 }

    @staticmethod
    def get_users():
        users = psutil.users()
        users_info = {}
        for user in users:
            users_info[user.name] = {
                'term': user.terminal,
                'host': user.host,
                'started': user.started,
                'pid': user.pid,
            }
        return users_info

USER = User()