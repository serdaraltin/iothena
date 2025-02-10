import psutil

from app.utils.base import BaseInfo


class Resource(BaseInfo):
    def __init__(self):
        self.cpu = self.get_cpu_info()
        self.memory = self.get_memory_info()
        self.disk = self.get_disk_info()
        self.battery = self.get_battery_info()

    @staticmethod
    def get_battery_info():
        battery = psutil.sensors_battery()
        if battery:
            return {
                'percent': battery.percent,
                'plugged': battery.power_plugged,
                'secsleft': battery.secsleft
            }
        return None

    @staticmethod
    def get_cpu_info():
        cpu_count = psutil.cpu_count(logical=True)
        cpu_usage = psutil.cpu_percent()
        cpu_freq = psutil.cpu_freq()

        return {
            'count': cpu_count,
            'used': cpu_usage,
            'freq': int(cpu_freq[0])
        }

    @staticmethod
    def get_memory_info():
        memory_info = psutil.virtual_memory()

        return {
            'total': round(memory_info.total / (1024 ** 3), 1),
            'used': round(memory_info.used / (1024 ** 3), 1),
            'free': round(memory_info.free / (1024 ** 3), 1),
            'percent': memory_info.percent
        }

    @staticmethod
    def get_disk_info():
        disk_info = psutil.disk_usage('/')

        return {
            'total': round(disk_info.total / (1024 ** 3), 1),
            'used': round(disk_info.used / (1024 ** 3), 1),
            'free': round(disk_info.free / (1024 ** 3), 1),
            'percent': disk_info.percent,
        }


RESOURCE = Resource()