import psutil

from app.utils.base import BaseInfo


class Thermal(BaseInfo):

    def __init__(self):
        self.sensors = self.get_sensors()
        self.cpu_temp = self.get_cpu_temperature()


    @staticmethod
    def get_sensors():
        sensors = psutil.sensors_temperatures()
        sensors_info = {}
        for sen in sensors:
            sensors_info[sen] = sensors[sen][0].current
        return sensors_info

    @staticmethod
    def get_cpu_temperature():
        sensors = psutil.sensors_temperatures()
        cpu_temp = sensors['cpu_thermal'][0][1]
        return cpu_temp

THERMAL = Thermal()