# IP Addressing Plan

## Purpose

This document defines the IPv4 addressing strategy for the Juniper SP/Enterprise Lab.

The goal is to assign addresses in a predictable way before configuration begins so that:

- Devices are easier to identify.
- VLAN subnets remain consistent.
- Point-to-point links are easy to troubleshoot.
- Routing protocols can be added later without redesigning the addressing scheme.
- Automation can reference predictable networks and addresses.
- Addressing decisions do not have to be recreated during every phase.

---

## Addressing Strategy

The lab will use separate address ranges based on network function.

| Address Space | Purpose |
|---|---|
| `10.10.0.0/16` | Enterprise LAN and VLAN networks |
| `10.20.0.0/16` | WAN / external test networks |
| `10.255.0.0/16` | Infrastructure and point-to-point transit networks |
| `10.255.255.0/24` | Loopbacks and router IDs |

This creates an addressing pattern that makes the purpose of an IP address easier to recognize.

---

## Original Baseline Topology

The original Phase 0 topology was:

`PC-LAN → FW-SRX → RTR-SRX → PC-WAN`

The original addressing plan used:

- `10.10.10.0/24` for the enterprise LAN
- `10.255.0.0/30` for the firewall-to-router transit network
- `10.20.20.0/24` for the WAN-side test network

The original EVE-NG `.unl` file remains preserved as the baseline topology.

---

## Planned Topology

The enterprise topology will expand to:

`PC-LAN → ACCESS-SW → DIST-SW → FW-SRX → RTR-SRX → PC-WAN`

Planned hostnames:

`LAB-PC-01 → LAB-SW-01 → LAB-SW-02 → LAB-FW-01 → LAB-RTR-01 → LAB-PC-02`

---

# Enterprise VLAN Addressing

Enterprise VLANs will receive subnets from the `10.10.0.0/16` address space.

| VLAN ID | VLAN Name | Subnet | Planned Gateway |
|---|---|---|---|
| 10 | USERS | `10.10.10.0/24` | `10.10.10.1` |
| 20 | SERVERS | `10.10.20.0/24` | `10.10.20.1` |
| 30 | MANAGEMENT | `10.10.30.0/24` | `10.10.30.1` |
| 40 | AUTOMATION | `10.10.40.0/24` | `10.10.40.1` |
| 99 | INFRASTRUCTURE | `10.10.99.0/24` | `10.10.99.1` |

The `.1` address is reserved as the default gateway for each VLAN.

---

## VLAN Gateway Placement

The current design intends for the distribution layer to eventually provide Layer 3 gateway functionality for enterprise VLANs.

Because the distribution switch is planned to be a Cisco device, these Layer 3 VLAN interfaces would normally be implemented as:

`SVIs — Switched Virtual Interfaces`

Examples:

- VLAN 10 → `10.10.10.1/24`
- VLAN 20 → `10.10.20.1/24`
- VLAN 30 → `10.10.30.1/24`
- VLAN 40 → `10.10.40.1/24`
- VLAN 99 → `10.10.99.1/24`

On Juniper switching platforms, the equivalent Layer 3 concept would commonly be an `IRB` interface.

The exact gateway placement will be finalized before configuration begins.

---

# Endpoint Addressing

## LAB-PC-01

`LAB-PC-01` represents an enterprise user endpoint in VLAN 10.

| Property | Value |
|---|---|
| VLAN | `10` |
| Network | `10.10.10.0/24` |
| Planned IP | `10.10.10.10/24` |
| Planned Default Gateway | `10.10.10.1` |

Traffic from this endpoint will travel through the access and distribution layers before reaching the enterprise firewall.

---

## LAB-PC-02

`LAB-PC-02` represents an endpoint located on the external/WAN side of the topology.

| Property | Value |
|---|---|
| Network | `10.20.20.0/24` |
| Planned IP | `10.20.20.10/24` |
| Planned Default Gateway | `10.20.20.1` |

---

# Firewall-to-Router Transit Network

A dedicated point-to-point network connects the enterprise firewall to the upstream routing-focused SRX.

Network:

`10.255.0.0/30`

| Device | Interface | Planned IP |
|---|---|---|
| LAB-FW-01 | `ge-0/0/1` | `10.255.0.1/30` |
| LAB-RTR-01 | `ge-0/0/0` | `10.255.0.2/30` |

Subnet information:

| Address | Purpose |
|---|---|
| `10.255.0.0` | Network address |
| `10.255.0.1` | LAB-FW-01 |
| `10.255.0.2` | LAB-RTR-01 |
| `10.255.0.3` | Broadcast address |

A `/30` provides two usable IPv4 addresses, making it appropriate for a two-device point-to-point link.

---

# WAN-Side Network

The WAN-side test network uses:

`10.20.20.0/24`

| Device | Interface | Planned IP |
|---|---|---|
| LAB-RTR-01 | `ge-0/0/1` | `10.20.20.1/24` |
| LAB-PC-02 | `eth0` | `10.20.20.10/24` |

Default gateway for `LAB-PC-02`:

`10.20.20.1`

---

# Distribution-to-Firewall Transit Network

The connection between `LAB-SW-02` and `LAB-FW-01` should use a separate Layer 3 transit network if the distribution switch performs inter-VLAN routing.

This network has not yet been assigned.

Planned format:

`10.255.x.x/30`

Example structure:

| Device | Interface | Planned IP |
|---|---|---|
| LAB-SW-02 | `TBD` | `TBD` |
| LAB-FW-01 | `ge-0/0/0` | `TBD` |

This addressing should be finalized after confirming the Layer 3 boundary between the distribution switch and firewall.

---

# Loopback and Router ID Addressing

The following block is reserved:

`10.255.255.0/24`

Loopback addresses will be assigned using `/32` prefixes.

Potential future assignments:

| Device | Loopback / Router ID |
|---|---|
| LAB-FW-01 | `10.255.255.1/32` |
| LAB-RTR-01 | `10.255.255.2/32` |
| LAB-SW-02 | `10.255.255.3/32` |

These addresses are reserved but should not be considered active until the related routing phase is implemented.

Loopbacks may later be used for:

- Router IDs
- OSPF
- BGP
- Management
- Automation targeting
- Monitoring
- Troubleshooting

---

# Addressing Summary

| Function | Address Range |
|---|---|
| Enterprise networks | `10.10.0.0/16` |
| USERS VLAN | `10.10.10.0/24` |
| SERVERS VLAN | `10.10.20.0/24` |
| MANAGEMENT VLAN | `10.10.30.0/24` |
| AUTOMATION VLAN | `10.10.40.0/24` |
| INFRASTRUCTURE VLAN | `10.10.99.0/24` |
| WAN networks | `10.20.0.0/16` |
| Current WAN test network | `10.20.20.0/24` |
| Infrastructure/transit links | `10.255.0.0/16` |
| Firewall-router transit | `10.255.0.0/30` |
| Loopbacks/router IDs | `10.255.255.0/24` |

---

# Addressing Rules

- Enterprise VLANs use addresses from `10.10.0.0/16`.
- WAN-side networks use addresses from `10.20.0.0/16`.
- Infrastructure transit links use addresses from `10.255.0.0/16`.
- Loopbacks use addresses from `10.255.255.0/24`.
- Enterprise VLAN default gateways reserve the `.1` address.
- Infrastructure point-to-point links should use small subnets such as `/30`.
- Loopback interfaces should use `/32` addresses.
- New addresses must be documented before they are configured.
- The IP addressing plan, VLAN plan, circuit map, and topology diagram should remain synchronized.

---

# Phase 0 Open Design Items

The following addressing decisions must be finalized before configuration begins:

- Distribution-to-firewall transit subnet
- Distribution-switch interface addressing
- Final enterprise VLAN gateway placement
- Exact switch management IP addresses
- Whether the access switch receives a management address in VLAN 30
- Whether LAB-FW-01 receives a dedicated management address
- Whether LAB-RTR-01 receives a dedicated management address
- Final loopback addresses
- Exact Cisco switch interfaces used in EVE-NG

Values that have not yet been architecturally decided should remain `TBD` rather than being assigned arbitrarily.
