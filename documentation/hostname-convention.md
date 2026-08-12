# Hostname Convention

## Naming Standard

Device hostnames will follow this format:

`<SITE>-<ROLE>-<NUMBER>`

Examples:

- `LAB-FW-01`
- `LAB-RTR-01`
- `LAB-SW-01`
- `LAB-SRV-01`
- `LAB-PC-01`

## Role Codes

| Code | Device Role |
|---|---|
| FW | Firewall |
| RTR | Router |
| SW | Switch |
| SRV | Server |
| PC | End Host |
| AUTO | Automation Server |

## Current Topology

| Current EVE-NG Name | Planned Hostname | Role |
|---|---|---|
| PC-LAN | LAB-PC-01 | Enterprise LAN client |
| FW-SRX | LAB-FW-01 | Juniper SRX firewall |
| RTR-SRX | LAB-RTR-01 | Juniper SRX acting as router |
| PC-WAN | LAB-PC-02 | WAN-side test client |

## Naming Rules

- Use uppercase hostnames.
- Use hyphens between fields.
- Device numbers use two digits.
- Hostnames identify device function, not IP address.
- New devices follow the same naming standard as the topology expands.
