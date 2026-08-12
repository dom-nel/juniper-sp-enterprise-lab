# VLAN Plan

## VLAN Strategy

VLANs will be used on the enterprise side of the lab to separate user, server, management, and infrastructure traffic.

## VLAN Table

| VLAN ID | Name | Purpose | Planned Subnet |
|---|---|---|---|
| 10 | USERS | Enterprise user/client network | 10.10.10.0/24 |
| 20 | SERVERS | Ubuntu and application servers | 10.10.20.0/24 |
| 30 | MANAGEMENT | Network device management | 10.10.30.0/24 |
| 40 | AUTOMATION | Automation and NetDevOps services | 10.10.40.0/24 |
| 99 | INFRASTRUCTURE | Infrastructure/service traffic | 10.10.99.0/24 |

## Current Phase 0 Usage

The current baseline topology does not yet contain an Ethernet switch or trunk links.

The current LAN segment:

PC-LAN → FW-SRX

will initially operate as a routed Layer 3 network using:

10.10.10.0/24

VLAN 10 will become the USERS VLAN when switching is introduced later in the project.

## Design Rules

- VLAN IDs remain consistent throughout the lab.
- VLAN names use uppercase descriptive names.
- Each VLAN receives its own IPv4 subnet.
- Inter-VLAN routing will be introduced when switching is added.
- Management traffic will remain logically separated from user traffic.
