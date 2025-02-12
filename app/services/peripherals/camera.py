import threading
import time
from typing import Dict, Optional
from app.models.peripherals.camera import CameraModel
from app.services.systems.config import CONFIG
from app.services.systems.logger import LOGGER


class CameraService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            return cls._instance

    def __repr__(self):
        return repr(self.__dict__)

    def __init__(self):
        self.cls_name = self.__class__.__name__
        self.initialized = False
        self.config = CONFIG.cameras
        self.cameras: Dict[str, CameraModel] = {}
        self._thread = None
        self._stop_event = threading.Event()

    def get_all_cameras_info(self):
        """Returns properties of all cameras."""
        return {name: camera.get_properties() for name, camera in self.cameras.items()}

    def get_all_cameras(self) -> Dict[str, CameraModel]:
        """Returns all camera instances."""
        return self.cameras

    def get_camera(self, name) -> Optional[CameraModel]:
        """Gets a specific camera by name."""
        return self.cameras.get(name)

    def initialize(self):
        """Initializes cameras from the configuration."""
        for camera in self.config['cameras']:
            self.cameras[camera['name']] = CameraModel.from_dict(camera)
        self.initialized = True
        LOGGER.info(f"Cameras initialized.")

    def run(self, stop_event):
        """Main loop to keep the service running."""
        LOGGER.info("Starting Camera Service...")
        self.initialize()
        while not stop_event.is_set():
            time.sleep(10)  # Adjust interval as needed

        LOGGER.info(f"Camera service stopped.")

    def start(self):
        """Starts the CameraService in a separate thread."""
        if self._thread and self._thread.is_alive():
            LOGGER.warning(f"Camera service is already running.")
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self.run, args=(self._stop_event,), daemon=True)
        self._thread.start()
        LOGGER.info(f"Camera service started.")

    def stop(self):
        """Stops the CameraService."""
        if not self._thread or not self._thread.is_alive():
            LOGGER.warning(f"Camera service is not running.")
            return

        LOGGER.info(f"Stopping camera service...")
        self._stop_event.set()
        self._thread.join()
        LOGGER.info(f"Camera service stopped.")

    def is_initialized(self):
        """Checks if the service is initialized."""
        return self.initialized


CAMERA_SERVICE = CameraService()
