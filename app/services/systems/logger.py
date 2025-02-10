import os
import logging
import logging.config
from app.services.systems.config import CONFIG

log_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
    'fatal': logging.FATAL
}

class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

class Logger(logging.Logger):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        self._logger = logging.getLogger(CONFIG.logging['name'])
        log_path = os.path.join(CONFIG.work_dir,CONFIG.logging['path'])
        os.makedirs(log_path, exist_ok=True)
        file_path = os.path.join(str(log_path), CONFIG.logging['file'])

        formatter = logging.Formatter(CONFIG.logging['format'])

        self._logger.setLevel(log_levels[CONFIG.logging['level']])

        if not self._logger.hasHandlers():
            handler = logging.FileHandler(str(file_path))
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def __repr__(self):
        return repr(self._logger)

    @property
    def logger(self):
        return self._logger

LOGGER = Logger().logger