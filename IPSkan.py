import subprocess
import argparse
import ipaddress
import socket
import platform
import sys

def get_network(): 
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        network = ipaddress.ip_network(f"{local_ip}/24", strict=False)
        return str(network.network_address) + "/24"
    except Exception:
        return"127.0.0.1/24"
    
    network = ipaddress.ip_network(f"{local_ip}/24", strict=False)
    return str(network.network_address) + "/24"
def ping_host(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-w', '1000', str(ip)]
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return resoult.returncode == 0
    except FileNotFoundError:
        print("Blad: program 'ping' nie zostal znaleziony w systemie.")
        sys.exit(1)
def scan_network(network_str):
    try:
        net = ipaddress.ip_network(network_str, strict=False)
    except ValueError as e:
        print(f"Blad: niepoprawny format sieci: {e}")
        sys.exit(1)
    print(f"Skanowanie sieci: {network_str}...")
    active_hosts = []
    for ip in net.hosts():
        if ping_host(ip):
            active_hosts.append(str(ip))

    return active_hosts