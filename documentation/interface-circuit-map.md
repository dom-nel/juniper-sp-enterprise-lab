# Interface and Circuit Mapping

## Current Topology

PC-LAN → FW-SRX → RTR-SRX → PC-WAN

## Interface Map

| Circuit ID | Device A | Interface A | Device B | Interface B | Network | Purpose |
|---|---|---|---|---|---|---|
| CKT-001 | PC-LAN | eth0 | FW-SRX | ge-0/0/0 | 10.10.10.0/24 | Enterprise LAN access |
| CKT-002 | FW-SRX | ge-0/0/1 | RTR-SRX | ge-0/0/0 | 10.255.0.0/30 | Firewall-to-router transit |
| CKT-003 | RTR-SRX | ge-0/0/1 | PC-WAN | eth0 | 10.20.20.0/24 | WAN-side test network |

## Device Interface Assignments

### LAB-FW-01

| Interface | Connected To | Purpose | Planned IP |
|---|---|---|---|
| ge-0/0/0 | PC-LAN | Inside / LAN | 10.10.10.1/24 |
| ge-0/0/1 | LAB-RTR-01 | Transit / Outside | 10.255.0.1/30 |

### LAB-RTR-01

| Interface | Connected To | Purpose | Planned IP |
|---|---|---|---|
| ge-0/0/0 | LAB-FW-01 | Transit | 10.255.0.2/30 |
| ge-0/0/1 | PC-WAN | WAN-side network | 10.20.20.1/24 |

## Circuit Naming Standard

Circuits will use the format:

`CKT-###`

Examples:

- CKT-001
- CKT-002
- CKT-003

Each circuit ID uniquely identifies a physical or logical connection in the lab.
