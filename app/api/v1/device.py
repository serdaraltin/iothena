from fastapi import Request

from app.api.v1.base import BaseApi
from app.services.systems.config import CONFIG
from app.utils.network import NETWORK

class DeviceApi(BaseApi):
    def __init__(self):

        self.device = CONFIG.device
        self.device['uuid'] = CONFIG.statics['uuid']
        self.device['ip_address'] = NETWORK.ip_addresses
        self.device['port'] = CONFIG.api['port']

    async def get(self):
        return self.device.to_json()

    async def update(self, request: Request):
        data = await request.json()

        for key, value in data.items():
            if value is not None:
                self.device[key] = value
        CONFIG.device.save()
        return {
            'message': f"Device info updated successfully",
            'device': self.device.to_json()
        }, 200


