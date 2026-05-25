#!/usr/bin/env python3
"""
Host discovery via ARP scanning and ICMP ping.
"""

import ipaddress
import subprocess
import threading
from scapy.all import ARP, Ether, srp

def arp_scan(network_cidr):
    """Send ARP requests to all IPs in the network and return live hosts."""
    print(f"[*] ARP scanning {network_cidr}...")
    # Create ARP request
    arp = ARP(pdst=network_cidr)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    # Send packet and receive response
    result = srp(packet, timeout=3, verbose=0)[0]
    hosts = []
    for sent, received in result:
        hosts.append({'ip': received.psrc, 'mac': received.hwsrc})
    print(f"[+] Found {len(hosts)} live hosts via ARP.")
    return hosts

def ping_sweep(network_cidr):
    """Optional ICMP ping sweep as fallback for non‑ARP networks."""
    net = ipaddress.ip_network(network_cidr, strict=False)
    live = []
    def ping(ip):
        try:
            output = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], 
                                    capture_output=True, timeout=2)
            if output.returncode == 0:
                live.append(str(ip))
        except:
            pass
    threads = []
    for ip in net.hosts():
        t = threading.Thread(target=ping, args=(ip,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print(f"[+] Found {len(live)} live hosts via ICMP ping.")
    return [{'ip': ip, 'mac': 'unknown'} for ip in live]
