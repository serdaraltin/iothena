import os
import logging
import logging.config
from app.services.systems.config import CONFIG
import colorlog

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
        self.service_config = CONFIG.services['logging']
        self.config = CONFIG.logging

        self.file_config = self.config['file']
        self.console_config = self.config['console']

        self._logger = logging.getLogger(self.config['name'])
        self._logger.setLevel(log_levels[self.file_config['level']])

        if self.service_config['enabled']:
            if self.service_config['file']['enabled']:
                self.setup_file_logger()
            if self.service_config['console']['enabled']:
                self.setup_console_logger()

    def setup_file_logger(self):
        log_path = os.path.join(CONFIG.work_dir, self.file_config['path'])
        os.makedirs(log_path, exist_ok=True)
        file_path = os.path.join(str(log_path), self.file_config['file'])

        formatter = logging.Formatter(self.file_config['format'])

        if not self._logger.hasHandlers():
            file_handler = logging.FileHandler(str(file_path))
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

    def setup_console_logger(self):

        log_formatter = logging.Formatter(
            self.console_config['format']
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self._logger.addHandler(console_handler)

        colored_formatter = colorlog.ColoredFormatter(
            self.console_config['format'],
            reset=self.console_config['reset'],
            log_colors={
                'DEBUG': self.console_config['colors']['debug'],
                'INFO': self.console_config['colors']['info'],
                'WARNING': self.console_config['colors']['warning'],
                'ERROR': self.console_config['colors']['error'],
                'CRITICAL': self.console_config['colors']['critical'],
            }
        )

        console_handler.setFormatter(colored_formatter)

    def __repr__(self):
        return repr(self._logger)

    @property
    def logger(self):
        return self._logger

# Global logger instance
LOGGER = Logger().logger
