#from uvicorn.main import Server
import uvicorn
from fastapi import FastAPI
from app.services.systems.config import CONFIG
from routes.api import routers

class APIService:

    def __init__(self):
        self._app = FastAPI()
        self._router = routers[CONFIG.api['router']]
        self._app.include_router(self._router)


    def start(self):
        uvicorn.run(self._app, host=CONFIG.api['host'], port=CONFIG.api['port'])

    @property
    def app(self):
        return self._app

API_SERVICE = APIService()