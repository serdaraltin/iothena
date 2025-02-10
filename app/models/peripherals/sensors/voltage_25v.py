from app.models.peripherals.sensors.base import BaseSensor


class VoltageSensor(BaseSensor):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self, config):
        super().__init__()
        self.device = config['device']
        self.min_voltage = config['range']['min']
        self.max_voltage = config['range']['max']

    def __repr__(self):
        return repr(self.__dict__)

    @staticmethod
    def get_value():
        return 0

    def get_percentage(self, voltage, _max_voltage=None):
        if _max_voltage is None:
            _max_voltage = self.max_voltage
        return round((voltage / _max_voltage) * 100, 2)

    def get_voltage(self, value=get_value()):
        voltage = (value / 32767.0) * self.max_voltage
        return voltage