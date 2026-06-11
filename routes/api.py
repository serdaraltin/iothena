import websocket
from fastapi import APIRouter

from app.api.v1.usb import UsbApi
from app.api.v1.camera import CameraApi
from app.api.v1.device import DeviceApi
from app.api.v1.network import NetworkApi
from app.api.v1.sensor import SensorApi
from app.api.v1.status import StatusApi
from app.api.v1.websocket import WebsocketApi

from app.services.systems.config import CONFIG
from app.services.systems.logger import LOGGER

# Base API URL from configuration
base_url = CONFIG.api['base_url']


class V1Router(APIRouter):
    """
    API v1 main router.

    Registers:
        - WebSocket APIs
        - Device APIs
        - Status APIs
        - Network APIs
        - Sensor APIs
        - Camera APIs

    Example:
        router = V1Router(prefix="/api/v1")
    """

    def __init__(self, prefix: str):
        """
        Initialize router.

        Args:
            prefix (str): Base route prefix.

        Example:
            V1Router(prefix="/api/v1")
        """
        super().__init__(prefix=prefix)
        self.add_routes()

    def add_routes(self):
        """
        Register all API routes.
        """

        # ==========================================================
        # WebSocket API
        # ==========================================================

        websocket_api = WebsocketApi()

        self.add_api_websocket_route("/ws/{client_id}", websocket_api.websocket_endpoint)  # Client websocket connection
        self.add_api_websocket_route("/ws", websocket_api.data)  # Generic realtime websocket endpoint


        usb_api = UsbApi()
        self.add_api_route("/usb", usb_api.get, methods=["GET"])
        # ==========================================================
        # Device API
        # ==========================================================

        device_api = DeviceApi()

        self.add_api_route("/device", device_api.get, methods=["GET"])  # Get device information
        self.add_api_route("/device", device_api.update, methods=["PATCH"])  # Update device configuration

        # ==========================================================
        # Status API
        # ==========================================================

        status_api = StatusApi()

        self.add_api_route("/device/status", status_api.get_status, methods=["GET"])  # Get full device status
        self.add_api_route("/device/status/{property}", status_api.get_property, methods=["GET"])  # Get single status property

        # ==========================================================
        # Network API
        # ==========================================================

        network_api = NetworkApi()

        self.add_api_route("/device/network", network_api.get_network_info, methods=["GET"])  # Get network information
        self.add_api_route("/device/network/{property}", network_api.get_property, methods=["GET"])  # Get network property

        # ==========================================================
        # Sensor API
        # ==========================================================

        sensor_api = SensorApi()

        self.add_api_route("/device/sensors", sensor_api.get_all_sensors, methods=["GET"])  # Get all sensors
        self.add_api_route("/device/sensors/{sensor_id}", sensor_api.get_sensor_data, methods=["GET"])  # Get sensor by ID

        # ==========================================================
        # Camera API
        # ==========================================================

        camera_api = CameraApi()

        self.add_api_route("/device/cameras", camera_api.get_all_cameras, methods=["GET"])  # Get all connected cameras
        self.add_api_route("/device/cameras/{camera_name}", camera_api.get_camera_info, methods=["GET"])  # Get camera information
        self.add_api_route("/device/cameras/{camera_name}/{property_name}", camera_api.get_camera_property, methods=["GET"])  # Get camera property
        self.add_api_route("/device/cameras/{camera_name}/capture", camera_api.capture_image, methods=["POST"])  # Capture image


# ==========================================================
# Router Registry
# ==========================================================

routers = {
    "v1": V1Router(prefix=f"{base_url}/v1"),
}