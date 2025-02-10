from app.services.systems.logger import LOGGER
from app.services.systems.config import CONFIG

class Ads1115:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            return cls._instance

    def __repr__(self):
        return repr(self.__dict__)

    def __init__(self, _config):

        if not _config['connected']:
            LOGGER.info('ADS1115 not connected')
            return

        #self.adc = Adafruit_ADS1x15.ADS1115()

        #peripherals property
        self.id = _config['id']
        self.connected = _config['connected']
        self.polling_interval = _config['polling_interval']
        self.peripherals_pins = _config['connection']['pins']

        #device property
        self.device = CONFIG.sub_loader(_config['device'])

        self.connection = self.device['connection']
        self.pins = self.connection['pins']

        #peripherals -> device
        for pin, value in self.peripherals_pins.items():
            if value['device']:
                _custom_properties = None
                if value['properties']:
                    _custom_properties = value['properties']

                value = CONFIG.sub_loader(value['device'])
                if _custom_properties:
                    for _property, property_value in _custom_properties.items():
                        value['properties'][_property] = property_value

            self.pins[pin] = value


