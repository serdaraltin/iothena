import re
import fcntl
import struct
import socket
import time
import subprocess
from scapy.all import sniff
from typing import Optional, List
from attr import dataclass
from scapy.layers.dot11 import Dot11Beacon, Dot11Elt, Dot11

from app.services.systems.logger import LOGGER

@dataclass
class WifiNetwork:
    """
    Represents a Wi-Fi network with relevant details such as SSID, BSSID, signal strength,
    channel, and encryption type.
    """
    ssid: str
    bssid: str
    signal_strength: int
    channel: int
    encryption: str

class WifiService:
    """
    A class to manage Wi-Fi interfaces, including connecting, disconnecting,
    scanning for available networks, and retrieving connection information.
    """

    def __repr__(self):
        return repr(self.__dict__)

    def __init__(self, interface: str = 'wlan0', auto_up: bool = True):
        """
        Initializes the Wi-Fi service, checks the interface state, and brings it up if necessary.

        Args:
            interface (str): The interface name (default: 'wlan0').
            auto_up (bool): Whether to automatically bring up the interface if it's down (default: True).
        """
        self.interface = interface
        self.wpa_supplicant_conf = f"/etc/wpa_supplicant/wpa_supplicant_{self.interface}.conf"
        self.interface_state = self.validate_interface()
        if self.interface_state == "down" and auto_up:
            LOGGER.info(f"Interface auto-up: Name={self.interface}")
            self.interface_up()

    def validate_interface(self) -> str:
        """
        Validates the current state of the network interface.

        Returns:
            str: "up" if the interface is up, "down" if it is down, or raises an error if the interface does not exist.
        """
        try:
            with open(f'/sys/class/net/{self.interface}/operstate', 'r') as f:
                state = f.read().strip()
                if state == 'down':
                    LOGGER.info(f"Interface down: Name={self.interface}")
                    return "down"
                elif state == 'up':
                    LOGGER.info(f"Interface up: Name={self.interface}")
                    return "up"
                else:
                    raise ValueError(f'Interface state unknown: Name={self.interface}')
        except FileNotFoundError:
            raise ValueError(f'Interface not found: Name={self.interface}')

    @staticmethod
    def rfkill_unblock() -> bool:
        """
        Unblocks the Wi-Fi interface using rfkill if it's blocked.

        Returns:
            bool: True if the unblocking was successful, False otherwise.
        """
        try:
            subprocess.run(["sudo", "rfkill", "unblock", "wifi"], check=True)
            LOGGER.info(f"RF-kill unblock wifi successful.")
            return True
        except subprocess.CalledProcessError:
            LOGGER.error(f"RF-kill unblock wifi failed.")
            return False

    def interface_up(self) -> bool:
        """
        Brings the network interface up using the `ip link` command.

        Returns:
            bool: True if the interface was successfully brought up, False otherwise.
        """
        try:
            result = subprocess.run(
                ["sudo", "ip", "link", "set", self.interface, "up"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Capture standard output and error output
            #output = result.stdout.strip() if result.stdout else "No output"
            #error_output = result.stderr.strip() if result.stderr else "No error output"

            LOGGER.info(f"Interface up: Name={self.interface}")
            return True
        except subprocess.CalledProcessError as e:
            # If the command fails, capture error output from exception
            error_output = e.stderr.strip() if e.stderr else "No error output"
            LOGGER.warning(f"Interface cannot be brought up: Name={self.interface}, Error: {error_output}")

            # Handle specific error conditions based on the output
            if "Operation not possible due to RF-kill" in error_output:
                LOGGER.warning("RF-kill detected. Attempting to unblock Wi-Fi...")
                if self.rfkill_unblock():
                    LOGGER.info("RF-kill unblocked, retrying interface up...")
                    return self.interface_up()  # Retry the operation

            elif "Device or resource busy" in error_output:
                LOGGER.warning("Device is currently busy. Please check the interface status.")
                return False

            elif "No such device" in error_output:
                LOGGER.error("No such device found. Please check the interface name.")
                return False

            else:
                LOGGER.error(f"Unexpected error: {error_output}")
                return False

    def get_ip_address(self) -> Optional[str]:
        """
        Retrieves the IP address of the current interface.

        Returns:
            str: The IP address of the interface, or None if it couldn't be determined.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packed_ip = fcntl.ioctl(
                sock.fileno(),
                0x8915,
                struct.pack('256s', self.interface.encode()[:15])
            )
            return socket.inet_ntoa(packed_ip[20:24])
        except OSError:
            LOGGER.error(f'Failed to get IP address: Name={self.interface}')
            return None

    def scan_network(self, timeout: int = 19) -> List[WifiNetwork]:
        """
        Scans for available Wi-Fi networks using Scapy.

        Args:
            timeout (int): The time in seconds to scan for networks.

        Returns:
            List[WifiNetwork]: A list of WifiNetwork objects representing the networks found.
        """
        networks = []

        def packet_handler(pkt):
            if pkt.haslayer(Dot11Beacon):
                ssid = pkt[Dot11Elt].info.decode() if pkt[Dot11Elt].info else "Hidden"
                bssid = pkt[Dot11].addr2
                signal_strength = pkt.dBm_AntSignal
                channel = int(ord(pkt[Dot11Elt:3].info))
                encryption = "WPA2" if pkt.sprintf(f"{Dot11Beacon:%Dot11Beacon.cap%}").find("privacy") != -1 else "Open"

                networks.append(
                    WifiNetwork(
                        ssid=ssid,
                        bssid=bssid,
                        signal_strength=signal_strength,
                        channel=channel,
                        encryption=encryption
                    )
                )

        try:
            sniff(iface=self.interface, prn=packet_handler, timeout=timeout)
            LOGGER.info(f"Found networks: Count={len(networks)}")
        except Exception as e:
            LOGGER.error(f"Failed to scan networks: {e}")

        return networks

    def get_current_network(self) -> Optional[WifiNetwork]:
        """
        Retrieves information about the currently connected Wi-Fi network.

        Returns:
            WifiNetwork: A WifiNetwork object representing the current network, or None if not connected.
        """
        try:
            result = subprocess.run(["sudo", 'iwconfig', self.interface], capture_output=True, text=True)
            output = result.stdout

            # Use regex to extract the required information
            ssid = re.search(r'ESSID:"([^"]+)"', output)
            bssid = re.search(r'Access Point: ([0-9A-Fa-f:]{17})', output)
            signal = re.search(r'Signal level=(-?\d+) dBm', output)
            channel = re.search(r'Channel:(\d+)', output)

            if ssid and bssid and signal and channel:
                return WifiNetwork(
                    ssid=ssid.group(1),
                    bssid=bssid.group(1),
                    signal_strength=int(signal.group(1)),
                    channel=int(channel.group(1)),
                    encryption="WPA2"  # Assuming WPA2 encryption for simplicity
                )
        except Exception as e:
            LOGGER.error(f"Failed to get current network: {e}")
        return None

    def is_connected(self) -> bool:
        """
        Checks if the device is currently connected to a network.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self.get_current_network() is not None

    def wait_for_connection(self, timeout: int = 30) -> bool:
        """
        Waits for the device to connect to a network within a specified timeout.

        Args:
            timeout (int): The maximum time (in seconds) to wait for connection.

        Returns:
            bool: True if connected within the timeout, False otherwise.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_connected():
                return True
            time.sleep(1)
        return False

    def connect(self, ssid: str, password: Optional[str] = None) -> bool:
        """
        Connects to a Wi-Fi network by writing configuration to wpa_supplicant.

        Args:
            ssid (str): The SSID of the network.
            password (str, optional): The network password, if required.

        Returns:
            bool: True if connected successfully, False otherwise.
        """
        try:
            with open(self.wpa_supplicant_conf, "w") as f:
                f.write(f"network={{\n")
                f.write(f"  ssid={ssid}\n")
                if password:
                    f.write(f"  psk={password}\n")
                else:
                    f.write(f"  key_mgmt=None\n")
                f.write(f"}}\n")

            subprocess.run([
                "sudo", "wpa_supplicant", "-B", "-i", self.interface, "-c", self.wpa_supplicant_conf,
            ], check=True)

            LOGGER.info(f"Connected to network: {ssid}")
            return True
        except subprocess.CalledProcessError as e:
            LOGGER.error(f"Failed to connect: Name={self.interface}, Error: {e}")
            return False

    def disconnect(self) -> bool:
        """
        Disconnects from the current network by killing wpa_supplicant and releasing the DHCP lease.

        Returns:
            bool: True if disconnected successfully, False otherwise.
        """
        try:
            subprocess.run(["sudo", "killall", "wpa_supplicant"], check=True)
            subprocess.run(["sudo", "dhclient", "-r", self.interface], check=True)

            LOGGER.info(f"Disconnected from network: {self.interface}")
            return True
        except subprocess.CalledProcessError as e:
            LOGGER.error(f"Failed to disconnect: Name={self.interface}, Error: {e}")
            return False
