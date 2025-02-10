import threading

from app.services.systems.logger import LOGGER


class ThreadService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ThreadService, cls).__new__(cls, *args, **kwargs)
            return cls._instance

    def __init__(self):
        self.cls_name = self.__class__.__name__
        self.threads = {}

    def get_threads(self):
        return {name: {"is_alive": thread.is_alive()} for name, thread in self.threads.items()}

    def start(self, target, name):
        try:
            stop_event = threading.Event()
            thread = threading.Thread(target=target, name=name, daemon=True)
            thread.daemon = True
            thread.start()

            self.threads[name] = {"thread": thread, "stop_event": stop_event}

            LOGGER.info(f"[{self.cls_name}] New process started: Name={name}, PID={thread.name}")
            return thread
        except Exception as e:
            LOGGER.error(f"[{self.cls_name}] Failed to start process: Name={name}, Exception={e}")

    def stop(self, name):
        if not name in self.threads:
            LOGGER.warning(f'[{self.cls_name}] Not found process: Name={name}')
            return False
        try:
            self.threads[name]["stop_event"].set()
            self.threads[name]["thread"].join()
            LOGGER.info(f'[{self.cls_name}] Stopped process: Name={self.threads[name]["name"]}')
            self.threads.pop(name)
            return
        except Exception as e:
            LOGGER.error(f'[{self.cls_name}] Failed to stop process: Name={name}, Exception={e}')
            return

    def stop_all(self):
        if not self.threads:
            LOGGER.info(f'[{self.cls_name}] Processes list is empty')
            return False
        try:
            for thread in self.threads.values():
                self.stop(thread["name"])
            self.threads.clear()
            LOGGER.info(f'[{self.cls_name}] Stopped all processes')
            return True
        except Exception as e:
            LOGGER.error(f'[{self.cls_name}] Failed to stop all process: Exception={e}')
            return False


THREAD_SERVICE = ThreadService()