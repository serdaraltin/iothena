import unittest
import os
from dotenv import load_dotenv

from app.services.networks.wifi import WifiService, WifiNetwork


class TestWifiService(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.wifi = WifiService(interface='wlan0')
        self.ssid = os.getenv('WIFI_SSID')
        self.password = os.getenv('WIFI_PASSWORD')


    def test_scan_network(self):
        networks = self.wifi.scan_network()
        self.assertIsInstance(networks, list)

        for network in networks:
            self.assertIsInstance(network, WifiNetwork)
            self.assertIsInstance(network.ssid, str)
            self.assertIsInstance(network.signal_strength, int)
            self.assertIsInstance(network.channel, int)
            self.assertIsInstance(network.encryption, str)
        print(f"Scanning completed")

    def test_connect_disconnect(self):
        self.assertTrue(self.wifi.connect(self.ssid, self.password))
        self.assertTrue(self.wifi.is_connected())
        print(f"Wifi is connected: {self.ssid}")

        current_network = self.wifi.get_current_network()
        self.assertIsNotNone(current_network)
        self.assertEqual(current_network.ssid, self.ssid)
        print(f"Connected to network: {current_network.ssid}")

        self.assertTrue(self.wifi.disconnect())
        self.assertFalse(self.wifi.is_connected())
        print(f"Disconnected from network: {current_network.ssid}")

    def test_wait_for_connection(self):
        self.assertTrue(self.wifi.connect(self.ssid, self.password))
        self.assertTrue(self.wifi.wait_for_connection(timeout=10))
        print(f"Wifi is connected: {self.ssid}")

        self.assertFalse(self.wifi.disconnect())
        print(f"Disconnected from network: {self.ssid}")
        self.assertFalse(self.wifi.wait_for_connection(timeout=5))
        print(f"Connected to network: {self.ssid}")

    def tearDown(self):
        if self.wifi.is_connected():
            self.wifi.disconnect()
        print(f"Disconnected from network: {self.ssid}")

if __name__ == '__main__':
    unittest.main()
