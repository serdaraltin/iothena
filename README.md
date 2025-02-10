# **iothena - IoT Framework Documentation**

## Overview

**iothena** is a comprehensive Internet of Things (IoT) framework designed to provide a foundation for creating a wide variety of IoT applications. Whether you are building smart homes, industrial IoT systems, or environmental monitoring solutions, **iothena** offers a flexible, scalable, and modular platform to get your project off the ground quickly.

It includes components for device management, sensor data collection, event-driven actions, machine learning integration, real-time notifications, and more, making it suitable for both small and large IoT solutions. **iothena** aims to be the go-to framework for any IoT-based application, giving you the ability to customize and extend as needed.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Core Features](#core-features)
3. [System Requirements](#system-requirements)
4. [Installation Guide](#installation-guide)
5. [Configuration Files](#configuration-files)
6. [API Documentation](#api-documentation)
7. [Sensor Integration](#sensor-integration)
8. [Event Handling and Alerts](#event-handling-and-alerts)
9. [Machine Learning Integration](#machine-learning-integration)
10. [Testing](#testing)
11. [Contributing](#contributing)
12. [License](#license)
13. [Contact Information](#contact-information)

---

## Project Structure

The structure of **iothena** follows a modular design to allow flexibility. Here’s an overview:

```
├── app                     # Core application logic
│   ├── api                 # REST API for device interaction, sensor data retrieval, etc.
│   ├── controller          # Controller for handling device and event logic
│   ├── events              # Event handling and triggers (e.g., alerts, device updates)
│   ├── helpers             # Helper functions for various utilities (e.g., time handling, data conversion)
│   ├── http                # HTTP handling for requests, middleware, and external integrations
│   ├── models              # Data models representing devices, sensors, notifications, etc.
│   ├── modules             # External modules (e.g., machine learning, image recognition)
│   ├── notifications       # Real-time notification system (e.g., Telegram alerts)
│   ├── services            # Core business logic (e.g., network, notification, sensor management)
│   ├── utils               # Utility functions (e.g., system, firmware management, network handling)
│   └── view                # Frontend components for UI interactions with the system
├── config                  # Configuration files (network, devices, alerts, etc.)
├── database                # Database connector and schema
├── docker                  # Docker configuration for containerized deployment
├── docs                    # Documentation files and requirements
├── logs                    # Log files for system diagnostics
├── main.py                 # Main entry point for the framework
├── public                  # Public resources (e.g., images, static files)
├── routes                  # API routing logic
├── script                  # Setup and installation scripts
├── storage                 # Persistent storage (e.g., database, device settings)
└── tests                   # Unit and integration tests
```

### Key Directories and Files

- **app/api**: The REST API for interaction with devices, sensors, and event management.
- **app/controllers**: Manages the flow of data between models and services.
- **app/events**: Event-driven logic for actions like sending notifications or triggering device actions.
- **app/models**: Data models like devices, sensors, events, and notifications.
- **app/services**: Core services managing business logic, such as networking and device control.
- **config**: YAML configuration files for devices, sensors, alerts, and more.
- **database**: Manages the database connection and schema for storing system data.
- **logs**: Logs for monitoring system activity and debugging.
- **routes**: API routes to handle various HTTP requests.
- **tests**: Unit and integration tests to ensure stability.

---

## Core Features

### 1. **Modular Architecture**

**iothena** is designed to be modular, allowing developers to pick and choose components to suit their specific use case. Some core modules include:

- **Sensor Integration**: Seamless support for sensors like temperature, humidity, and motion.
- **Device Management**: Easily add and configure IoT devices.
- **Real-Time Notifications**: Instant alerts via services like Telegram.
- **Machine Learning**: Integration with AI models for tasks like object detection and data analysis.

### 2. **Event-Driven System**

The framework supports defining custom events that trigger actions in response to changes in sensor data, device statuses, or other conditions. For example, if a sensor value exceeds a threshold, an event can trigger an action such as activating an actuator or sending an alert.

### 3. **AI and Machine Learning Integration**

**iothena** integrates machine learning models like YOLO for object detection and offers tools for analyzing sensor data and making intelligent decisions.

### 4. **Cross-Platform Compatibility**

The framework is compatible with popular IoT devices such as Raspberry Pi, Arduino, and ESP32, making it easy to deploy on various hardware platforms.

---

## System Requirements

To get started with **iothena**, ensure you meet the following prerequisites:

- **Python 3.12+**
- **Docker** (recommended for containerized deployment)
- **Database**: PostgreSQL, MySQL, or SQLite
- **External Libraries**:
    - `Flask` (for API handling)
    - `TensorFlow` (for machine learning models)
    - `OpenCV` (for image processing)
    - `requests` (for HTTP requests)

---

## Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/iothena.git
cd iothena
```

### 2. Install Dependencies

Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the environment configuration file:

```bash
cp .env.example .env
```

Then, edit the `.env` file with the correct settings for your environment, such as database credentials and API keys.

### 4. Run the Application

You can run **iothena** locally:

```bash
python main.py
```

Alternatively, use Docker for containerized deployment:

```bash
docker-compose up --build
```

### 5. Test the Framework

Run the tests to ensure everything is working:

```bash
pytest
```

---

## API Documentation

The **iothena** API allows you to interact with devices, sensors, and more.

### Base URL

The API base URL is `http://localhost:5000/api/v1/`.

### Example Endpoints

- **GET /api/v1/devices**  
  Retrieves a list of registered devices and their statuses.

- **POST /api/v1/devices**  
  Adds a new device to the network.

- **GET /api/v1/sensors/{sensor_id}**  
  Fetches the latest data from a specific sensor.

- **POST /api/v1/alerts**  
  Manually triggers an alert based on a predefined condition.

---

## Sensor Integration

Integrating sensors into **iothena** is simple. Supported sensors include:

- **Temperature and Humidity Sensors**
- **Motion Sensors**
- **Voltage Sensors**

You can extend the framework to support additional sensors by creating new sensor modules in the `app/models/sensors/` directory.

---

## Event Handling and Alerts

Custom events can be created to trigger actions based on sensor data, device status, or other conditions.

For example, an event could be created to send a notification when a sensor value exceeds a threshold:

```python
def temperature_threshold_event(sensor_data):
    if sensor_data["temperature"] > 30:
        send_alert("Temperature exceeded threshold!")
```

---

## Machine Learning Integration

**iothena** supports AI models such as YOLO for object detection. Here's how to use YOLO for object detection with a camera feed:

```python
from app/modules/yolo import YOLOService

yolo_service = YOLOService()
detections = yolo_service.detect_objects(camera_feed)
```

---

## Testing

**iothena** includes unit and integration tests. You can run the tests using `pytest`:

```bash
pytest tests
```

You can also write your own tests in the `tests/` directory.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Write tests for the new functionality.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Contact Information

For further assistance or inquiries, please contact us via email at [seyupaltin@gmail.com](seyupaltin@gmail.com).
