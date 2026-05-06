import argparse, subprocess, ipaddress, socket, platform, sys

def get_network():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return str(ipaddress.IPv4Interface(f"{s.getsockname()[0]}/24").network)
    except:
        return "192.168.0.0/24"

def ping_host(ip):
    sys_name = platform.system().lower()
    if sys_name == 'windows':
        cmd = ['ping', '-n', '1', '-w', '1000', str(ip)]
    else:
        cmd = ['ping', '-c', '1', '-W', '1', str(ip)]
    
    try:
        return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    except FileNotFoundError:
        print("Błąd: Brak programu ping.")
        sys.exit(1)

def scan_network(network):
    try:
        net = ipaddress.IPv4Network(network, strict=False)
        return [str(ip) for ip in net.hosts()]
    except ValueError:
        print(f"Błąd: Niepoprawny format sieci: {network}")
        sys.exit(1)

def print_results(results, network, output_file):
    active = [ip for ip in results if ping_host(ip)]
    out = f"Skanowana siec: {network}\nAktywne hosty:\n"
    out += "\n".join(f"{i}. {ip}" for i, ip in enumerate(active, 1)) if active else "Brak aktywnych hostów."
    
    print(out)
    if output_file:
        try:
            with open(output_file, 'w') as f: f.write(out + "\n")
        except Exception as e: print(f"Błąd zapisu: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--network")
    parser.add_argument("--output")
    args = parser.parse_args()

    try:
        net = args.network or get_network()
        print(f"Skanowanie {net}...")
        print_results(scan_network(net), net, args.output)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Błąd: {e}")

if __name__ == "__main__":
    main()