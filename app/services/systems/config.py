import os
import yaml

WORKING_DIR = os.getcwd()
CONFIG_DIR = os.path.join(WORKING_DIR, 'config')

class ConfigLoader:
    extension = 'yaml'

    def __init__(self, name, folder_path=CONFIG_DIR):
        self.name = name
        self.file_path = os.path.join(folder_path, name) + '.' + self.extension
        self.config = self.load()[self.name]

    def to_json(self):
        return self.config

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value

    def load(self):
        if not os.path.exists(self.file_path):
            #LOGGER.error(f"[{self.__class__.__name__}] Config file not found: File = {self.file_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.file_path}")
        with open(self.file_path, 'r') as file:
            try:
                #LOGGER.info(f"[{self.__class__.__name__}] Loading config file: File = {self.file_path}")
                return yaml.load(file, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                #LOGGER.error(f"[{self.__class__.__name__}] Error parsing config file: File = {self.file_path}, Exception = {exc}")
                raise ValueError(f"Error parsing configuration file {self.file_path}: {exc}")

    def save(self):
        if not os.path.exists(self.file_path):
            #LOGGER.error(f"[{self.__class__.__name__}] Config file not found: File = {self.file_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.file_path}")
        with open(self.file_path, 'w') as file:
            try:
                #LOGGER.info(f"[{self.__class__.__name__}] Saving config file: File = {self.file_path}")
                yaml.dump({self.name:self.config}, file)
                file.close()
            except yaml.YAMLError as exc:
                #LOGGER.error(f"[{self.__class__.__name__}] Error parsing config file: File = {self.file_path}, Exception = {exc}")
                raise ValueError(f"Error parsing configuration file {self.file_path}: {exc}")


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            return cls._instance

    def __repr__(self):
        return repr(self.__dict__)

    def __init__(self):
        self.loader_class = ConfigLoader

        self.work_dir = WORKING_DIR
        self.storage_dir = os.path.join(WORKING_DIR, 'storage')

        self.statics = self.loader_class('statics')
        self.api = self.loader_class('api')
        self.logging = self.loader_class('logging')
        self.peripherals = self.loader_class('peripherals')
        self.services = self.loader_class('services')
        self.device = self.loader_class('device')
        self.backend = self.loader_class('backend')
        self.cameras = self.loader_class('cameras')
        self.time = self.loader_class('time')
        self.notification = self.loader_class('notification')

    def sub_loader(self, path):
        path = path.split('.')
        config_name = path[-1]
        path = path[:-1]
        folder_path = os.path.join(CONFIG_DIR, *path)
        return self.loader_class(config_name,folder_path)

    def merge(self, right, other):
        pass

CONFIG = Config()