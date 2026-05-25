#!/usr/bin/env python3
"""
Generate interactive HTML network map using pyvis.
"""

from pyvis.network import Network

def generate_html_map(G, filename='reports/network_map.html'):
    """Create an interactive HTML file from networkx graph."""
    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')
    net.set_options("""
    var options = {
        "nodes": {
            "shape": "dot",
            "size": 20,
            "color": {
                "border": "#00ffcc",
                "background": "#006699"
            },
            "font": {
                "color": "#ffffff"
            }
        },
        "edges": {
            "color": "#00ffcc",
            "smooth": false
        },
        "physics": {
            "enabled": true,
            "stabilization": true
        }
    }
    """)
    for node, attrs in G.nodes(data=True):
        net.add_node(node, title=f"MAC: {attrs.get('mac', 'N/A')}")
    for edge in G.edges():
        net.add_edge(edge[0], edge[1])
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    net.save_graph(filename)
    print(f"[+] Interactive map saved to {filename}")