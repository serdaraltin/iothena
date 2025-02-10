from app.services.systems.config import CONFIG

from datetime import datetime
import pytz

class TimeHelper:
    def __init__(self):
        self.config = CONFIG.time
        self.timezone = pytz.timezone(self.config['timezone'])
        self.ntp = self.config['ntp']
        self.manual_override = self.config['manual_override']

    def get_current_time(self):
        current_time = datetime.now(self.timezone)
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        return formatted_time

    def get_current_time_for_file(self):
        return datetime.now(self.timezone).strftime("%Y%m%d_%H%M%S%f")


TIME_HELPER = TimeHelper()
