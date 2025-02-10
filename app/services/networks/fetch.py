from app.services.systems.logger import LOGGER
from app.services.networks.request import REQUEST_SERVICE


class FetchService(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        try:
            self.bad_words = REQUEST_SERVICE.get('bad-words')
        except Exception as e:
            LOGGER.error(f"{e}")

FETCH_SERVICE = FetchService()