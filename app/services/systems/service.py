import uuid

from app.services.services import SERVICES
from app.services.systems.config import CONFIG
from app.services.systems.logger import LOGGER
from app.services.systems.thread import THREAD_SERVICE

class Services:
    def __repr__(self):
        return repr(self.services)

    def __init__(self, thread_service):
        """Initialize the Services class with a thread service manager."""
        self.config = CONFIG.services
        self.thread_service = thread_service
        self.services = {}
        self.threads = {}

        # Load services from SERVICES list
        self.load_from_list()

    def load_from_list(self):
        """Load services configurations from the SERVICES list."""
        try:
            for service_info in SERVICES:
                service_name = service_info["name"]
                service_object = service_info["service"]
                self.add_service(service_name, service_object)
        except Exception as e:
            LOGGER.error(f"Error loading services from list: {e}")

    def add_service(self, name, service):
        """Add a new service to the dictionary with a unique name."""
        if name in self.services:
            raise ValueError(f"Service with name '{name}' already exists.")
        self.services[name] = {"service": service, "status": "Stopped"}
        LOGGER.info(f"Service added: Name={name}")
        return name

    def remove_service(self, service_name):
        """Remove a service using its unique name."""
        if service_name in self.services:
            del self.services[service_name]
        else:
            raise ValueError(f"Service with name '{service_name}' not found.")

    def start_service(self, service_name):
        """Start a specific service using its unique name."""
        if service_name in self.services:
            service = self.services[service_name]["service"]
            thread_name = f"service({service_name})"
            result = self.thread_service.start_thread(target=service.run, thread_name=thread_name)
            if result["status"] == "started":
                self.threads[service_name] = {"thread_name": thread_name, "stop_event": result["stop_event"]}
                # Update service status to "Running"
                self.services[service_name]["status"] = "Running"
            return result
        else:
            raise ValueError(f"Service with name '{service_name}' not found.")

    def stop_service(self, service_name):
        """Stop a specific service using its unique name."""
        if service_name in self.threads:
            stop_event = self.threads[service_name]["stop_event"]
            thread_name = self.threads[service_name]["thread_name"]
            result = self.thread_service.stop_thread(thread_name, stop_event)
            if result["status"] == "stopped":
                del self.threads[service_name]
                # Update service status to "Stopped"
                self.services[service_name]["status"] = "Stopped"
            return result
        else:
            raise ValueError(f"Service with name '{service_name}' is not running.")

    def start_all(self):
        """Start all registered services."""
        LOGGER.info("Starting all services...")
        results = []
        for service in self.services:
            service_config = self.config[service]
            if service_config["enabled"]:
                results.append(self.start_service(service))
                LOGGER.info(f"Service started: Name={service}")
            else:
                LOGGER.info(f"Service disabled: Name={service}")
        return results

    def stop_all(self):
        """Stop all running services."""
        LOGGER.info("Stopping all services...")
        results = []
        for service_name in list(self.threads.keys()):
            results.append(self.stop_service(service_name))
        return results

    def list_services(self):
        """Return a dictionary with all services, their names, and their status."""
        return {
            service_name: {
                "status": self.services[service_name]["status"]
            }
            for service_name in self.services
        }

    def get_service(self, service_name):
        return self.services[service_name]["service"]

    def get_service_status(self, service_name):
        return self.services[service_name]["status"]


# Create the Services instance
SERVICE = Services(THREAD_SERVICE)
