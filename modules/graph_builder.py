#!/usr/bin/env python3
"""
Build networkx graph from host list and SNMP neighbor data.
"""

import networkx as nx

def build_graph(hosts, neighbors):
    """hosts: list of dicts {'ip':..., 'mac':...}
       neighbors: dict {ip: [neighbor_ip_or_name]}
    """
    G = nx.Graph()
    # Add all hosts as nodes
    for h in hosts:
        G.add_node(h['ip'], type='host', mac=h.get('mac', 'unknown'))
    # Add neighbor edges
    for src_ip, nbr_list in neighbors.items():
        for nbr in nbr_list:
            G.add_edge(src_ip, nbr, type='snmp_neighbor')
    return G

def generate_inventory_csv(G, filename='reports/inventory.csv'):
    """Export nodes as CSV with IP, MAC, and degree."""
    import csv
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['IP', 'MAC', 'Degree'])
        for node, attrs in G.nodes(data=True):
            writer.writerow([node, attrs.get('mac', 'unknown'), G.degree(node)])
    print(f"[+] Inventory saved to {filename}")