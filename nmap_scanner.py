# Port Scanner using nmap module
import nmap
import sys
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <IP_ADDRESS>")
    sys.exit(1)
target = sys.argv[1]
scanner = nmap.PortScanner()
print(f"Scanning {target}...")
scanner.scan(target, '1-1024')
for port in scanner[target]['tcp']:
    state = scanner[target]['tcp'][port]['state']
    if state == 'open':
        print(f"Port {port} is OPEN")
