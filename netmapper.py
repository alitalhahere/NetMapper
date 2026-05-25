#!/usr/bin/env python3
"""
NetMapper – Network Topology Mapper & Asset Discovery
"""

import sys
import argparse
from modules.discovery import arp_scan, ping_sweep
from modules.snmp_query import get_lldp_neighbors, get_cdp_neighbors
from modules.graph_builder import build_graph, generate_inventory_csv
from modules.visualiser import generate_html_map

def main():
    parser = argparse.ArgumentParser(description='NetMapper - Network Topology Mapper')
    parser.add_argument('network', help='Network CIDR (e.g., 192.168.1.0/24)')
    parser.add_argument('--snmp-community', default='public', help='SNMP community string')
    parser.add_argument('--output', default='reports', help='Output directory')
    args = parser.parse_args()

    print("\n=== NetMapper ===")
    # 1. Discover hosts
    hosts = arp_scan(args.network)
    if not hosts:
        print("[!] ARP scan found no hosts, trying ICMP ping sweep...")
        hosts = ping_sweep(args.network)
    if not hosts:
        print("[-] No live hosts found. Exiting.")
        sys.exit(1)

    # 2. For each host, attempt SNMP neighbour query
    neighbors = {}
    for h in hosts:
        ip = h['ip']
        print(f"[*] Querying SNMP on {ip}...")
        lldp = get_lldp_neighbors(ip)
        if lldp:
            neighbors[ip] = [n['name'] for n in lldp]
        else:
            cdp = get_cdp_neighbors(ip)
            if cdp:
                neighbors[ip] = cdp
            else:
                neighbors[ip] = []

    # 3. Build graph
    G = build_graph(hosts, neighbors)

    # 4. Export inventory CSV
    generate_inventory_csv(G, f"{args.output}/inventory.csv")

    # 5. Generate interactive HTML map
    generate_html_map(G, f"{args.output}/network_map.html")

    print(f"\n[+] Done. Open {args.output}/network_map.html in a browser.")

if __name__ == '__main__':
    main()