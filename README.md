# 🗺️ NetMapper

**Network Topology Mapper & Asset Discovery – ARP scan, SNMP neighbours, interactive visualisation.**

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Network](https://img.shields.io/badge/Network-Scanner-orange)

## 🎯 Purpose

NetMapper discovers live hosts on your network, queries SNMP for LLDP/CDP neighbour relationships, and builds an interactive map of your infrastructure. Perfect for asset inventory, network documentation, and security audits.

## 📦 Installation

```bash
git clone https://github.com/alitalhahere/NetMapper.git
cd NetMapper
pip install -r requirements.txt
```

** Note: Requires snmpget/snmpwalk (install via sudo apt install snmp on Debian/Kali).**

## 🚀 Usage

```bash
sudo python netmapper.py 192.168.1.0/24 --snmp-community public --output ./reports
```
- sudo needed for ARP scanning (raw sockets).
- --snmp-community – default public; change if your devices use a different community.
- --output – directory for CSV and HTML output.

## 🖼️ Example Output

- Interactive map: reports/network_map.html (drag nodes, zoom, hover for MAC addresses).

- Inventory CSV: reports/inventory.csv (IP, MAC, degree).

## 🔧 Dependencies

- scapy – ARP scanning

- networkx + pyvis – graph building & HTML visualisation

- snmp-cmds – SNMP neighbour queries

## 📜 License

- MIT

## 👤 Author

Ali Talha – 