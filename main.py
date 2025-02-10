from app.services.networks.api import API_SERVICE
from app.services.notification.telegram import TELEGRAM_SERVICE
from app.services.peripherals.camera import CAMERA_SERVICE
from app.services.systems.logger import LOGGER
from app.services.systems.thread import THREAD_SERVICE

if __name__ == '__main__':


    try:
        THREAD_SERVICE.start(target=API_SERVICE.start, name=API_SERVICE.__class__.__name__)
        THREAD_SERVICE.start(target=TELEGRAM_SERVICE.start, name=API_SERVICE.__class__.__name__)
        #THREAD_SERVICE.start(target=CAMERA_SERVICE.start, name=CAMERA_SERVICE.__class__.__name__)

        #data = FETCH_SERVICE.bad_words


        while True:
            pass

    except KeyboardInterrupt:
        LOGGER.info(f"[{__name__}] Exiting...")
    finally:
        THREAD_SERVICE.stop_all()

