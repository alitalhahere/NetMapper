#!/usr/bin/env python3
"""
Query SNMP for LLDP/CDP neighbour tables and bridge forwarding tables.
Uses snmp-cmds (requires snmpget/snmpwalk installed on system).
"""

import subprocess

def snmp_walk(ip, oid, community='public'):
    """Perform SNMP walk and return list of values."""
    try:
        cmd = ['snmpwalk', '-v', '2c', '-c', community, ip, oid]
        output = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        lines = output.stdout.strip().split('\n')
        # Extract values after '=' sign
        values = []
        for line in lines:
            if '=' in line:
                parts = line.split('=')
                if len(parts) > 1:
                    values.append(parts[1].strip())
        return values
    except Exception as e:
        print(f"[-] SNMP walk failed for {ip}: {e}")
        return []

def get_lldp_neighbors(ip):
    """Retrieve LLDP neighbour device IDs (sysName) via SNMP."""
    # LLDP remote sysName OID: 1.0.8802.1.1.2.1.4.1.1.9
    oid = '1.0.8802.1.1.2.1.4.1.1.9'
    sys_names = snmp_walk(ip, oid)
    # Also get chassis ID to correlate
    chassis_oid = '1.0.8802.1.1.2.1.4.1.1.4'
    chassis = snmp_walk(ip, chassis_oid)
    neighbors = []
    for i, name in enumerate(sys_names):
        neighbor = {'name': name, 'chassis': chassis[i] if i < len(chassis) else 'unknown'}
        neighbors.append(neighbor)
    return neighbors

def get_cdp_neighbors(ip):
    """Retrieve CDP neighbour device IDs via SNMP (Cisco)."""
    # CDP cache device ID OID: 1.3.6.1.4.1.9.9.23.1.2.1.1.6
    oid = '1.3.6.1.4.1.9.9.23.1.2.1.1.6'
    return snmp_walk(ip, oid)
