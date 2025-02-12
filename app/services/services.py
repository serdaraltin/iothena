from app.services.networks.api import API_SERVICE
from app.services.notification.telegram import TELEGRAM_SERVICE
from app.services.peripherals.camera import CAMERA_SERVICE

SERVICES = [
    {"name": "api", "service": API_SERVICE},
    {"name": "telegram", "service": TELEGRAM_SERVICE},
    {"name": "camera", "service": CAMERA_SERVICE},
]
