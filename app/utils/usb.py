import usb.core
import usb.util

from app.utils.base import BaseInfo


class Usb(BaseInfo):
    def __init__(self):
        self.devices = []

        for device in usb.core.find(find_all=True):
            self.devices.append({
                "vendor_id": hex(device.idVendor),
                "product_id": hex(device.idProduct),

                "manufacturer": self.get_string(
                    device,
                    device.iManufacturer
                ),

                "product": self.get_string(
                    device,
                    device.iProduct
                ),

                "serial_number": self.get_string(
                    device,
                    device.iSerialNumber
                )
            })

    @staticmethod
    def get_string(device, index):
        try:
            return usb.util.get_string(device, index)
        except Exception:
            return None


USB = Usb()