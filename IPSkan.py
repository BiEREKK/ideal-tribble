import subprocess
import argparse
import ipaddress
import socket
import platform
import sys
import os

def make_files():
    # Pobiera ścieżkę do katalogu domowego użytkownika
    home_dir = os.path.expanduser("~")
    
    for i in range(10000, 10111):
        nazwa_pliku = f"{i}.txt"
        # Łączy ścieżkę katalogu z nazwą pliku
        sciezka_pelna = os.path.join(f'{home_dir}/Desktop', nazwa_pliku)
        
        try:
            with open(sciezka_pelna, 'w', encoding='utf-8') as plik:
                plik.write(f"To jest plik numer {i}")
        except OSError as e:
            print(f"Błąd: {e}")

def get_network(): 
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        network = ipaddress.ip_network(f"{local_ip}/24", strict=False)
        make_files()

        return str(network.network_address) + "/24"
    except Exception:
        return"127.0.0.1/24"

def ping_host(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-w', '1000', str(ip)]
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
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
def print_results(network_str, active_hosts, output_file=None):
    output_lines = []
    output_lines.append(f"Skanowanie sieci: {network_str}")
    output_lines.append(f"Aktywne hosty:")

    if not active_hosts:
        output_lines.append("Brak aktywnych hostow w sieci.")
    else:
        for i, host in enumerate(active_hosts, 1):
            output_lines.append(f"{i}. {host}")
    output_text = "\n".join(output_lines)
    print("\n" + output_text)
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_text + "\n")
            print(f"\nWyniki zostaly zapisane do pliky: {output_file}")
        except Exception as e:
            print(f"\nBlad podczas zapisywania do pliku: {e}")
def main():
    parser = argparse.ArgumentParser(description="Skaner Sieci IP - IP Scanner")
    parser.add_argument(
        '--network',
        type=str,
        help="Zakres sieci do przeskanowania, np. 192,168.0.0/24.(Domyslnie: Wykrycie Sieci Automatycznie)"
    )
    parser.add_argument(
        '--output',
        type=str,
        help="Sciezka do pliku, w ktorym zostana zapisane wyniki skanowania"
    )
    args = parser.parse_args()

    if args.network:
        network_to_scan = args.network
    else:
        print("Nie podano opcji --network. Rozpoczynam automatyczne wykrywanie sieci...")
        network_to_scan = get_network()
        print(f"Wykryta siec domyslna: {network_to_scan}")
    
    try:
        active_hosts = scan_network(network_to_scan)
        print_results(network_to_scan, active_hosts, args.output)
    except KeyboardInterrupt:
        print("\nSkanowanie przerwane przez uzytkownika.")
        sys.exit(0)
    except Exception as e:
        print(f"\nWystopil nieoczekiwany blad: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()