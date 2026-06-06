# Host Discovery Tool
# - Finds your gateway IP
# - Determines IP class
# - Discovers live hosts on the network
import socket
import subprocess
import platform
import nmap
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))       # connect to Google DNS (doesn't send data)
    local_ip = s.getsockname()[0]    # read what IP was used
    s.close()
    return local_ip
def get_gateway_ip():
    os_type = platform.system()

    if os_type == "Windows":
        output = subprocess.check_output("ipconfig", shell=True).decode()
        for line in output.splitlines():
            if "Default Gateway" in line:
                parts = line.split(":")
                if len(parts) == 2 and parts[1].strip():
                    return parts[1].strip()

    else:  
        output = subprocess.check_output("ip route", shell=True).decode()
        for line in output.splitlines():
            if "default" in line:
                return line.split()[2]   # e.g. "default via 192.168.1.1 dev eth0"

    return "Not found"
def get_ip_class(ip):
    first_octet = int(ip.split('.')[0])   # take the first number e.g. 192

    if 1 <= first_octet <= 126:
        return "A"
    elif 128 <= first_octet <= 191:
        return "B"
    elif 192 <= first_octet <= 223:
        return "C"
    elif 224 <= first_octet <= 239:
        return "D (Multicast)"
    elif 240 <= first_octet <= 255:
        return "E (Reserved)"
    else:
        return "Unknown"
def discover_hosts(network):
    scanner = nmap.PortScanner()
    print(f"\n🔍 Scanning network: {network} (this may take a moment...)\n")

    # -sn = ping scan (no port scan, just checks who is alive)
    scanner.scan(hosts=network, arguments='-sn')

    live_hosts = scanner.all_hosts()
    return live_hosts

if __name__ == "__main__":

    my_ip     = get_local_ip()
    gateway   = get_gateway_ip()
    ip_class  = get_ip_class(my_ip)
    network = '.'.join(my_ip.split('.')[:3]) + '.0/24'

    print("=" * 40)
    print("       HOST DISCOVERY TOOL")
    print("=" * 40)
    print(f"  Your IP     : {my_ip}")
    print(f"  Gateway IP  : {gateway}")
    print(f"  IP Class    : Class {ip_class}")
    print(f"  Network     : {network}")
    print("=" * 40)
    hosts = discover_hosts(network)

    print(f"  Live Hosts Found: {len(hosts)}")
    print("-" * 40)
    for host in hosts:
        print(f"{host}")
    print("=" * 40)
