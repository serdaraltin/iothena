import socket
import psutil
import uuid
from app.utils.base import BaseInfo


class Network(BaseInfo):
    def __repr__(self):
        self.update()
        return repr(self.__dict__)

    def __init__(self):
        self.established_ports = None
        self.listen_ports = None
        self.active_connections = None
        self.dns_server = None
        self.dns = None
        self.status = None
        self.traffic = None
        self.all_addresses = None
        self.ip_addresses = None
        self.default_gateways = None
        self.mac_interfaces = None
        self.mac_uuid = None
        self.interfaces = None
        self.hostname = None
        self.update()

    def update(self):
        self.hostname = socket.gethostname()
        self.interfaces = self.get_interfaces()

        self.mac_uuid = self.get_mac_address()
        self.mac_interfaces = self.get_mac_addresses()

        self.default_gateways = self.get_default_gateway()

        self.ip_addresses = self.get_ip_addresses()
        self.all_addresses = self.get_all_addresses()

        self.traffic = self.get_traffic()
        self.status = self.get_status()

        self.dns = self.get_dns()
        self.dns_server = self.get_dns_server()

        self.active_connections = self.get_active_connections()
        self.listen_ports = self.get_listen_ports()
        self.established_ports = self.get_established_ports()


    @staticmethod
    def get_established_ports():
        connections = psutil.net_connections(kind="inet")
        active_connections = []
        for connection in connections:
            if connection.status == "ESTABLISHED":
                active_connections.append(connection.laddr[1])
        return active_connections

    @staticmethod
    def get_listen_ports():
        connections = psutil.net_connections(kind="inet")
        active_connections = []
        for connection in connections:
            if connection.status == "LISTEN":
                active_connections.append( connection.laddr[1])
        return active_connections

    @staticmethod
    def get_active_connections():
        connections = psutil.net_connections(kind="inet")
        active_connections = []
        for connection in connections:
            active_connections.append(
                {
                    "local_address": connection.laddr,
                    "remote_address": connection.raddr,
                    "status": connection.status,
                }
            )
        return active_connections

    @staticmethod
    def get_all_addresses():
        interfaces = {}
        for interface, addrs in psutil.net_if_addrs().items():
            addresses = []
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    addresses.append(f"IPv4: {addr.address}")
                elif addr.family == socket.AF_INET6:
                    addresses.append(f"IPv6: {addr.address}")
                elif addr.family == psutil.AF_LINK:
                    addresses.append(f"MAC: {addr.address}")
            interfaces[interface] = addresses
        return interfaces

    @staticmethod
    def get_ip_by_interface(_interface):
        interface_info = []
        for interface, addrs in  psutil.net_if_addrs().items():
            if _interface == interface:
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        interface_info.append(f"IPv4: {addr.address}")
                    elif addr.family == socket.AF_INET6:
                        interface_info.append(f"IPv6: {addr.address}")
                    elif addr.family == psutil.AF_LINK:
                        interface_info.append(f"MAC: {addr.address}")
        return interface_info

    @staticmethod
    def get_interfaces():
        interfaces = []
        for interface, addrs in psutil.net_if_addrs().items():
            interfaces.append(interface)
        return interfaces

    @staticmethod
    def get_ip_addresses():
        ip_addresses = []
        for interface, addresses in psutil.net_if_addrs().items():
            for addr in addresses:
                if addr.family == socket.AF_INET:
                    ip_addresses.append(addr.address)
        return ip_addresses

    @staticmethod
    def get_mac_address():

        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 8 * 6, 8)][::-1])
        return str(mac_address)

    @staticmethod
    def get_mac_addresses():
        mac_addresses = {}
        for interface, addresses in psutil.net_if_addrs().items():
            for addr in addresses:
                mac_addresses[interface] = addr.address
        return mac_addresses

    @staticmethod
    def get_traffic():
        net_io = psutil.net_io_counters(pernic=True)
        traffic = {}
        for interface, stats in net_io.items():
            traffic[interface] = {
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv,
                "packets_sent": stats.packets_sent,
                "packets_recv": stats.packets_recv,
            }
        return traffic

    @staticmethod
    def get_status():
        status = {}
        for interface, addrs in psutil.net_if_stats().items():
            status[interface] = "UP" if addrs.isup else "DOWN"
        return status

    @staticmethod
    def get_default_gateway():
        getaways = psutil.net_if_addrs()
        gateway_info = psutil.net_if_stats()
        return getaways, gateway_info

    @staticmethod
    def get_dns():
        dns_servers = []

        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if line.startswith('nameserver'):
                    dns_servers.append(line.split()[1])
        return dns_servers

    @staticmethod
    def get_dns_server():
        dns_servers = []
        return dns_servers
        try:
            dns_info = socket.getaddrinfo('google.com', None)
            for server in dns_info:
                dns_servers.append(server[4][0])
        except socket.gaierror:
            raise Exception("Can not resolve the host address")
        return dns_servers

NETWORK = Network()