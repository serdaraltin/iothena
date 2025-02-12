import asyncio
import uvicorn
import threading
from fastapi import FastAPI, WebSocket, Depends
from routes.api import routers
from app.services.systems.logger import LOGGER
from app.services.systems.config import CONFIG

class APIService:
    def __init__(self):
        self.config = CONFIG.api
        self._app = FastAPI()
        self._router = routers[self.config['router']]
        self._app.include_router(self._router)
        self._server_thread = None
        self._stop_event = threading.Event()

    def run(self, stop_event):
        """Runs the FastAPI application in a thread."""
        config = uvicorn.Config(self._app,
                                host=self.config['host'],
                                port=self.config['port'],
                                loop="asyncio",
                                ws="websockets"
                                )
        server = uvicorn.Server(config)

        LOGGER.info("Starting API server...")

        async def server_task():
            await server.serve()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        while not stop_event.is_set():
            loop.run_until_complete(server_task())

        loop.close()
        LOGGER.info("API server stopped.")

    def start(self):
        """Starts the API service in a separate thread."""
        if self._server_thread and self._server_thread.is_alive():
            LOGGER.warning("API server is already running.")
            return

        self._stop_event.clear()
        self._server_thread = threading.Thread(target=self.run, args=(self._stop_event,), daemon=True)
        self._server_thread.start()
        LOGGER.info("API server started.")

    def stop(self):
        """Stops the API service."""
        if not self._server_thread or not self._server_thread.is_alive():
            LOGGER.warning("API server is not running.")
            return

        LOGGER.info("Stopping API server...")
        self._stop_event.set()
        self._server_thread.join()
        LOGGER.info("API server stopped.")

    @property
    def app(self):
        return self._app


API_SERVICE = APIService()
