from app.api.v1.base import BaseApi
from app.utils.network import NETWORK


class NetworkApi(BaseApi):

    def __init__(self):
        self.network = NETWORK

    @staticmethod
    async def get_network_info():
        return NETWORK


    async def get_property(self, property):
        if not hasattr(NETWORK, property):
            return {"error": f"No such property: {property}"}

        return {property: getattr(NETWORK, property)}