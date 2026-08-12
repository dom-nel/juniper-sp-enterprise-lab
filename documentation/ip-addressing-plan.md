# IP Addressing Plan

## Addressing Strategy

- Enterprise/LAN networks: `10.10.x.x`
- WAN/customer-side networks: `10.20.x.x`
- Infrastructure/transit networks: `10.255.x.x`
- Loopbacks/router IDs: reserved from `10.255.255.0/24`

## Current Topology

PC-LAN → FW-SRX → RTR-SRX → PC-WAN

## IP Addressing Table

| Segment | Network | Device | Interface | Planned IP |
|---|---|---|---|---|
| LAN | 10.10.10.0/24 | PC-LAN | eth0 | 10.10.10.10/24 |
| LAN | 10.10.10.0/24 | FW-SRX | ge-0/0/0 | 10.10.10.1/24 |
| FW-Router Transit | 10.255.0.0/30 | FW-SRX | ge-0/0/1 | 10.255.0.1/30 |
| FW-Router Transit | 10.255.0.0/30 | RTR-SRX | ge-0/0/0 | 10.255.0.2/30 |
| WAN | 10.20.20.0/24 | RTR-SRX | ge-0/0/1 | 10.20.20.1/24 |
| WAN | 10.20.20.0/24 | PC-WAN | eth0 | 10.20.20.10/24 |

## Default Gateways

- PC-LAN: `10.10.10.1`
- PC-WAN: `10.20.20.1`

## Reserved Infrastructure Space

- Transit links: `10.255.0.0/16`
- Loopbacks and router IDs: `10.255.255.0/24`
