# Learning the nmap module - simple demo
import nmap
import sys

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <IP_ADDRESS>")
    sys.exit(1)

target = sys.argv[1]
scanner = nmap.PortScanner()

print(f"\nScanning {target}...\n")
scanner.scan(target, '1-1024', arguments='-sV')
for port in scanner[target]['tcp']:
    info = scanner[target]['tcp'][port]

    if info['state'] == 'open':
        name    = info['name']       # service name  e.g. http
        product = info['product']    # software      e.g. Apache
        version = info['version']    # version       e.g. 2.4.51

        print(f"Port {port:5d} | {name:10} | {product} {version}")
print(f"\nScan info: {scanner.scaninfo()}")
print(f"All hosts found: {scanner.all_hosts()}")
