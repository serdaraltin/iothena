from app.models.peripherals.sensors.voltage_25v import VoltageSensor

sensors = {
    'voltage_sensor': VoltageSensor,
}

class SensorService:

    def __repr__(self):
        return repr(self.__dict__)

    def __init__(self):
        pass



