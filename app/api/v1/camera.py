from app.api.v1.base import BaseApi
from app.services.peripherals.camera import CAMERA_SERVICE


class CameraApi(BaseApi):

    def __init__(self):
        self.cameras = CAMERA_SERVICE.cameras

    @staticmethod
    async def get_all_cameras():
        return CAMERA_SERVICE.get_all_cameras_info()


    @staticmethod
    async def get_camera_info(camera_name):
        camera = CAMERA_SERVICE.get_camera(camera_name)
        if camera is None:
            return {
                'error': f"Camera not found: {camera_name}",
                'status': 404
            }
        return camera.get_properties()

    @staticmethod
    async def get_camera_property(camera_name, property_name):
        camera = CAMERA_SERVICE.get_camera(camera_name)
        if camera is None:
            return {
                'message': 'Camera not found',
                'status': 404
            }
        properties = camera.get_properties()
        if property_name not in properties:
            return {
                'error': f'No such property: {property_name}',
                'status': 404
            }
        return properties[property_name]

    @staticmethod
    def capture_image(camera_name):
        pass
