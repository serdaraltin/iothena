from typing import Dict

from app.models.peripherals.camera import CameraModel
from app.services.systems.config import CONFIG


class CameraService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            return cls._instance

    def __repr__(self):
        return repr(self.__dict__)

    def __init__(self):
        self.initialized = False
        self.config = CONFIG.cameras
        self.cameras: Dict[str, CameraModel] = {}

    def get_all_cameras_info(self):
        return {
            name:
                camera.get_properties()
            for name, camera in self.cameras.items()
        }

    def get_all_cameras(self) -> Dict[str, CameraModel]:
        return self.cameras

    def get_camera(self, name) -> CameraModel | None:
        if name not in self.cameras:
            return None
        return self.cameras[name]

    def start(self):
        for camera in self.config['cameras']:
            self.cameras[camera['name']] = CameraModel.from_dict(camera)
        self.initialized = True

    def is_initialized(self):
        return self.initialized


CAMERA_SERVICE = CameraService()