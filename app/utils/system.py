import os
import platform

from app.utils.base import BaseInfo


class System(BaseInfo):
    def __init__(self):
        self.name = os.name
        self.system = platform.system()
        self.node = platform.node()
        self.release = platform.release()
        self.machine = platform.machine()
        self.version = platform.version()
        self.processor = platform.processor()
        self.release = platform.release()
        self.architecture = platform.architecture()
        self.platform = platform.platform()


SYSTEM = System()