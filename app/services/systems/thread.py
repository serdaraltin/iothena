import threading
from app.services.systems.logger import LOGGER

class ThreadService:
    @staticmethod
    def start_thread(target, thread_name):
        """Starts a new thread for the given service."""
        try:
            stop_event = threading.Event()
            thread = threading.Thread(target=target, name=thread_name, daemon=True, args=(stop_event,))
            thread.start()
            LOGGER.info(f"Thread started: Name={thread_name}")
            return {"status": "started", "thread_name": thread_name, "stop_event": stop_event}
        except Exception as e:
            LOGGER.error(f"Failed to start thread: Name={thread_name}, Exception={e}")
            return {"status": "failed", "error": str(e)}

    @staticmethod
    def stop_thread(thread_name, stop_event):
        """Stops the given thread by setting its stop event."""
        try:
            stop_event.set()
            LOGGER.info(f"Thread stopped: Name={thread_name}")
            return {"status": "stopped", "thread_name": thread_name}
        except Exception as e:
            LOGGER.error(f"Failed to stop thread: Name={thread_name}, Exception={e}")
            return {"status": "failed", "error": str(e)}

THREAD_SERVICE = ThreadService()
