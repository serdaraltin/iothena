from app.api.v1.base import BaseApi
from app.helpers.time import TIME_HELPER
from app.services.systems.thread import THREAD_SERVICE
from app.utils.firmware import FIRMWARE
from app.utils.network import NETWORK
from app.utils.resource import RESOURCE
from app.utils.system import SYSTEM
from app.utils.thermal import THERMAL

class StatusApi(BaseApi):

    def __init__(self):
        self.resource = RESOURCE
        self.system = SYSTEM
        self.thermal = THERMAL
        self.network = NETWORK
        self.firmware = FIRMWARE
        self.process = THREAD_SERVICE.get_threads()

    @staticmethod
    async def get_processes():
        return THREAD_SERVICE.get_threads()

    @staticmethod
    async def get_status():

        health_data = [
            THERMAL.get_cpu_temperature(),
            RESOURCE.get_cpu_info()['used'],
            RESOURCE.get_memory_info()['used'],
            RESOURCE.get_disk_info()['used']
        ]
        if RESOURCE.get_battery_info():
            health_data.append(RESOURCE.get_battery_info()['percent'])
        health = sum(health_data) / len(health_data)

        status = {
            "health": round(health, 2),
            "temperature": THERMAL.get_cpu_temperature(),
            "battery_level": RESOURCE.get_battery_info(),
            "cpu_usage": RESOURCE.get_cpu_info()['used'],
            "memory_usage": RESOURCE.get_memory_info()['used'],
            "disk_usage": RESOURCE.get_disk_info()['used'],
            "last_checked": TIME_HELPER.get_current_time(),
            "services": THREAD_SERVICE.get_threads(),
        }
        return status

    async def get_property(self, property):
        if not hasattr(self, property):
            return {"error": f"No such property: {property}"}

        return {property: getattr(self, property)}
