import unittest
import os
import json
from config.config_manager import Config


class TestConfig(unittest.TestCase):
    TEST_CONFIG_PATH = "test_config.json"

    @classmethod
    def setUpClass(cls):
        # Override the default CONFIG_PATH for testing
        Config.CONFIG_PATH = cls.TEST_CONFIG_PATH

        # Ensure test configuration is fresh
        if os.path.exists(cls.TEST_CONFIG_PATH):
            os.remove(cls.TEST_CONFIG_PATH)

    @classmethod
    def tearDownClass(cls):
        # Cleanup test configuration file after all tests
        if os.path.exists(cls.TEST_CONFIG_PATH):
            os.remove(cls.TEST_CONFIG_PATH)

    def setUp(self):
        # Initialize Config for each test
        self.config = Config()

    def test_load_fresh_config(self):
        """Test if fresh configuration is loaded when file is absent."""
        self.assertTrue(os.path.exists(self.TEST_CONFIG_PATH))
        with open(self.TEST_CONFIG_PATH, "r") as f:
            data = json.load(f)
        self.assertEqual(data, Config.FRESH_CONFIG)

    def test_modify_and_save_config(self):
        """Test modifying and saving configuration."""
        self.config.device.name = "Test-Device"
        self.config.settings.debug_mode = True

        Config.dump(self.config.__dict__)

        with open(self.TEST_CONFIG_PATH, "r") as f:
            data = json.load(f)

        self.assertEqual(data["device"]["name"], "Test-Device")
        self.assertTrue(data["settings"]["debug_mode"])

    def test_reload_config(self):
        """Test reloading configuration from file."""
        modified_config = Config.FRESH_CONFIG.copy()
        modified_config["device"]["name"] = "Reloaded-Device"

        with open(self.TEST_CONFIG_PATH, "w") as f:
            json.dump(modified_config, f, indent=4)

        reloaded_config = Config()

        self.assertEqual(reloaded_config.device.name, "Reloaded-Device")

    def test_nested_config_access(self):
        """Test access to nested configuration fields."""
        self.assertEqual(self.config.settings.logging.file_path, "logs/device.log")
        self.assertEqual(self.config.pins.gpio["temperature_sensor"], 4)
        self.assertEqual(self.config.sensors.temperature_sensor["type"], "DHT22")

    def test_default_values(self):
        """Test if default values are correctly assigned."""
        self.assertEqual(self.config.device.name, "RaspberryPi-IoT-Device")
        self.assertEqual(self.config.device.firmware_version, "1.0.0")
        self.assertEqual(self.config.alerts.thresholds["temperature"]["max"], 50)


if __name__ == "__main__":
    unittest.main()
