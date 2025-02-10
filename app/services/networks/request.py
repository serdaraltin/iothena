import requests

from app.services.systems.logger import LOGGER
from app.services.systems.config import CONFIG

class RequestService:
    def __init__(self, headers=None):
        self.cls_name = self.__class__.__name__
        self.prefix = CONFIG.backend['prefix']
        self.host = CONFIG.backend['host']
        self.port = CONFIG.backend['port'] or None
        self.base_url = CONFIG.backend['base_url']
        self.router = CONFIG.backend['router']

        if self.port:
            self.api_url = f"{self.prefix}://{self.host}:{self.port}/{self.base_url}/{self.router}"
        else:
            self.api_url = f"{self.prefix}://{self.host}/{self.base_url}/{self.router}"

        self.headers = headers or {"Content-Type": "application/json"}

    def get(self, url, params=None):
        try:
            response = requests.get(f"{self.api_url}/{url}", headers=self.headers, params=params)
            response.raise_for_status()
            LOGGER.info(f"[{self.cls_name}] GET={self.api_url}/{url}")
            return response.json()
        except requests.exceptions.HTTPError as err:
            LOGGER.error(f"[{self.cls_name}] Request failed: {err}")
            return err.response

    def post(self, url, data=None):
        try:
            response = requests.post(f"{self.api_url}/{url}", headers=self.headers, json=data)
            response.raise_for_status()
            LOGGER.info(f"[{self.cls_name}] POST={self.api_url}/{url}")
            return response.json()
        except requests.exceptions.HTTPError as err:
            LOGGER.error(f"[{self.cls_name}] Request failed: {err}")
            return err.response

    def put(self, url, data=None):
        try:
            response = requests.put(f"{self.api_url}/{url}", headers=self.headers, json=data)
            response.raise_for_status()
            LOGGER.info(f"[{self.cls_name}] PUT={self.api_url}/{url}")
            return response.json()
        except requests.exceptions.HTTPError as err:
            LOGGER.error(f"[{self.cls_name}] Request failed: {err}")
            return err.response

    def delete(self, url):
        try:
            response = requests.delete(f"{self.api_url}/{url}", headers=self.headers)
            response.raise_for_status()
            LOGGER.info(f"[{self.cls_name}] DELETE={self.api_url}/{url}")
            return response.json()
        except requests.exceptions.HTTPError as err:
            LOGGER.error(f"[{self.cls_name}] Request failed: {err}")

REQUEST_SERVICE = RequestService()