from fastapi import Request

from app.api.v1.base import BaseApi
from app.utils.usb import USB


class UsbApi(BaseApi):
    def __init__(self):
        self.devices = USB

    async def  get(self):
        return self.devices
