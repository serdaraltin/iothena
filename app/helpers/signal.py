import sys

from app.services.systems.logger import LOGGER
from app.services.systems.service import SERVICE

class SignalHelper:
    @staticmethod
    def signal_handler(sig, frame):
        """Signal handler for graceful shutdown on keyboard interrupt."""
        LOGGER.info(f"Signal {sig} received. Shutting down gracefully...")
        LOGGER.info("Services are shutting down gracefully...")
        SERVICE.stop_all()
        sys.exit(0)  # Exit the program after shutting down services
