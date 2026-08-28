# VLAN Plan

> **Future design reference:** VLANs and switching are not implemented in the active four-node Phase 1 topology. This document is retained as design input for a later switching phase and must not be read as completed work.

## Purpose

This document defines how Layer 2 networks will be segmented across the enterprise portion of the lab.

The VLAN plan provides a consistent reference for:

- VLAN IDs
- VLAN names
- VLAN purposes
- Associated IPv4 subnets
- Access-layer VLAN behavior
- Distribution-layer VLAN behavior
- Trunk relationships between switches
- Future Layer 3 gateway placement

The VLAN plan should remain synchronized with the IP addressing plan, interface/circuit map, topology diagram, and device configurations.

---

## VLAN Strategy

VLANs will separate different types of enterprise traffic into individual Layer 2 broadcast domains.

The planned enterprise VLANs are:

| VLAN ID | Name | Purpose | Planned Subnet |
|---|---|---|---|
| 10 | USERS | Enterprise user/client network | `10.10.10.0/24` |
| 20 | SERVERS | Ubuntu and application servers | `10.10.20.0/24` |
| 30 | MANAGEMENT | Network device management | `10.10.30.0/24` |
| 40 | AUTOMATION | Automation and NetDevOps services | `10.10.40.0/24` |
| 99 | INFRASTRUCTURE | Infrastructure and network-service traffic | `10.10.99.0/24` |

Each VLAN receives its own IPv4 subnet.

---

## Original Baseline Topology

The original Phase 0 topology was:

`PC-LAN → FW-SRX → RTR-SRX → PC-WAN`

The original topology did not contain an Ethernet switching layer.

Because no switches or trunk links existed, the original LAN segment operated as a simple routed network:

`10.10.10.0/24`

The original EVE-NG `.unl` file remains preserved as the baseline topology.

---

## Planned Enterprise Topology

The enterprise side of the topology will expand to:

`PC-LAN → ACCESS-SW → DIST-SW → FW-SRX → RTR-SRX → PC-WAN`

Using planned hostnames:

`LAB-PC-01 → LAB-SW-01 → LAB-SW-02 → LAB-FW-01 → LAB-RTR-01 → LAB-PC-02`

This introduces two distinct switching roles:

- Access layer
- Distribution layer

---

# Access Layer

## LAB-SW-01

`LAB-SW-01` represents the enterprise access switch.

The access layer is where endpoints connect to the network.

An endpoint normally connects to an access port assigned to a specific VLAN.

For example:

`LAB-PC-01 → Access Port → VLAN 10`

LAB-PC-01 therefore becomes a member of the USERS VLAN.

### Planned Access-Layer Behavior

| Connection | Port Type | VLAN Behavior |
|---|---|---|
| LAB-PC-01 → LAB-SW-01 | Access | VLAN 10 |
| Future server → LAB-SW-01 | Access | VLAN 20 |
| Future management endpoint | Access | VLAN 30 |
| Future automation server | Access | VLAN 40 |
| LAB-SW-01 → LAB-SW-02 | Trunk | Multiple VLANs |

The exact physical switch interfaces will be documented in the interface/circuit map after the Cisco switch image is finalized.

---

## Access Ports

An access port normally carries traffic for one VLAN.

Example logical configuration:

`PC-LAN → LAB-SW-01 → VLAN 10`

The connected endpoint does not need to understand VLAN tagging.

The access switch associates traffic arriving on that port with VLAN 10.

Planned endpoint VLAN membership:

| Endpoint Type | VLAN |
|---|---|
| Enterprise users | VLAN 10 |
| Servers | VLAN 20 |
| Management devices | VLAN 30 |
| Automation systems | VLAN 40 |

---

# Distribution Layer

## LAB-SW-02

`LAB-SW-02` represents the enterprise distribution or aggregation switch.

The distribution layer receives traffic from the access layer and provides an aggregation point before enterprise traffic reaches the firewall.

### Planned Distribution-Layer Responsibilities

- Receive multiple VLANs from access switches.
- Maintain VLAN separation.
- Aggregate access-layer connectivity.
- Provide the foundation for inter-VLAN routing.
- Provide Layer 3 gateway interfaces if the final design places gateways at the distribution layer.
- Forward enterprise traffic toward the firewall.
- Provide a foundation for future routing and redundancy exercises.

---

## Access-to-Distribution Trunk

The connection between:

`LAB-SW-01 ↔ LAB-SW-02`

will operate as an IEEE 802.1Q trunk.

The trunk allows multiple VLANs to cross the same physical link.

### Planned Trunk VLANs

| VLAN ID | VLAN Name | Planned on Trunk |
|---|---|---|
| 10 | USERS | Yes |
| 20 | SERVERS | Yes |
| 30 | MANAGEMENT | Yes |
| 40 | AUTOMATION | Yes |
| 99 | INFRASTRUCTURE | Yes |

The final allowed-VLAN list will be configured explicitly when the switching phase begins.

---

# Inter-VLAN Routing

Devices in different VLANs cannot communicate through Layer 2 switching alone.

For example:

`VLAN 10 USERS`

cannot directly communicate with:

`VLAN 20 SERVERS`

without a Layer 3 device routing between those subnets.

The planned design is to investigate placing the enterprise VLAN gateways at the distribution layer.

If LAB-SW-02 performs this function, the gateways could be:

| VLAN | Subnet | Planned Gateway |
|---|---|---|
| VLAN 10 | `10.10.10.0/24` | `10.10.10.1` |
| VLAN 20 | `10.10.20.0/24` | `10.10.20.1` |
| VLAN 30 | `10.10.30.0/24` | `10.10.30.1` |
| VLAN 40 | `10.10.40.0/24` | `10.10.40.1` |
| VLAN 99 | `10.10.99.0/24` | `10.10.99.1` |

Because LAB-SW-02 is planned as a Cisco switch, these Layer 3 VLAN interfaces would normally be called:

`SVIs — Switched Virtual Interfaces`

On a Juniper switching platform, a similar Layer 3 VLAN gateway function would commonly use an:

`IRB — Integrated Routing and Bridging interface`

The final gateway placement must be confirmed before configuration begins.

---

# VLAN 10 — USERS

## Purpose

VLAN 10 represents enterprise user and workstation traffic.

Planned subnet:

`10.10.10.0/24`

Planned default gateway:

`10.10.10.1`

Initial endpoint:

`LAB-PC-01`

This VLAN provides the first user-facing network in the lab.

---

# VLAN 20 — SERVERS

## Purpose

VLAN 20 represents application and Ubuntu server workloads.

Planned subnet:

`10.10.20.0/24`

Planned default gateway:

`10.10.20.1`

Future systems may include:

- Ubuntu application servers
- Web servers
- DNS services
- Monitoring systems
- Lab services

This VLAN separates server workloads from normal user endpoints.

---

# VLAN 30 — MANAGEMENT

## Purpose

VLAN 30 represents network-management traffic.

Planned subnet:

`10.10.30.0/24`

Planned default gateway:

`10.10.30.1`

Potential devices using this network include:

- LAB-SW-01
- LAB-SW-02
- LAB-FW-01
- LAB-RTR-01

Potential management services may later include:

- SSH
- NETCONF
- SNMP
- Syslog
- Monitoring
- Configuration management

Management traffic should remain logically separated from normal user traffic.

---

# VLAN 40 — AUTOMATION

## Purpose

VLAN 40 represents automation and NetDevOps systems.

Planned subnet:

`10.10.40.0/24`

Planned default gateway:

`10.10.40.1`

Potential systems include:

- Automation server
- Ansible controller
- Python automation tools
- API clients
- Configuration backup services
- CI/CD-related services

This VLAN creates a dedicated network for systems that programmatically interact with network devices.

---

# VLAN 99 — INFRASTRUCTURE

## Purpose

VLAN 99 is reserved for infrastructure and network-service traffic.

Planned subnet:

`10.10.99.0/24`

Planned default gateway:

`10.10.99.1`

The exact services placed in this VLAN will be determined as the topology develops.

VLAN 99 should not automatically be treated as a native VLAN solely because of its VLAN number.

Its role must be explicitly defined before configuration.

---

# VLAN Traffic Flow Example

A future user traffic flow may look like:

`LAB-PC-01`

↓ Access port in VLAN 10

`LAB-SW-01`

↓ 802.1Q trunk carrying VLAN 10

`LAB-SW-02`

↓ Layer 3 gateway / routing

`LAB-FW-01`

↓ Security policy enforcement

`LAB-RTR-01`

↓ WAN routing

`LAB-PC-02`

This demonstrates how Layer 2 switching, Layer 3 routing, security, and WAN connectivity work together.

---

# Access Layer vs Distribution Layer

The same VLAN may exist on both switches, but the switches perform different jobs.

| Function | Access Switch | Distribution Switch |
|---|---|---|
| Connect endpoints | Primary function | Usually no |
| Assign endpoints to VLANs | Yes | Usually no |
| Carry VLAN trunks | Yes | Yes |
| Aggregate multiple access switches | No | Yes |
| Perform inter-VLAN routing | Usually not in this lab | Planned |
| Host VLAN gateways | No in planned design | Potentially yes |
| Forward traffic toward firewall | Indirectly | Yes |

The difference is primarily the role of the switch in the architecture, not a different type of VLAN.

---

# VLANs and CoS

Class of Service (CoS) and VLANs are related networking concepts but perform different functions.

VLANs provide:

- Layer 2 segmentation
- Broadcast-domain separation
- Logical network membership

CoS/QoS provides:

- Traffic classification
- Prioritization
- Queueing
- Congestion handling
- Service differentiation

An access switch may eventually apply CoS policies to endpoint traffic, but CoS is not what makes an access VLAN different from a distribution-layer VLAN.

CoS will be documented separately when QoS is introduced into the project.

---

# VLAN Design Rules

- VLAN IDs remain consistent throughout the enterprise topology.
- VLAN names use uppercase descriptive names.
- Each enterprise VLAN receives its own IPv4 subnet.
- Endpoint-facing interfaces use access mode where appropriate.
- Switch-to-switch links use 802.1Q trunks where multiple VLANs must cross the connection.
- Trunks should explicitly define which VLANs are allowed.
- Management traffic remains logically separated from user traffic.
- Automation traffic remains logically separated from normal user traffic.
- VLAN 1 should not be intentionally used for production lab services unless a later design requires it.
- VLAN configuration must remain synchronized with the IP addressing plan.
- VLAN configuration must remain synchronized with the interface/circuit map.
- VLAN changes must be reflected in the topology documentation.

---

# Phase 0 Open Design Items

The following VLAN decisions should be finalized before switch configuration begins:

- Exact Cisco access-switch platform
- Exact Cisco distribution-switch platform
- Physical access-port assignments
- Physical trunk-port assignments
- Final allowed VLAN list on trunks
- Enterprise VLAN gateway placement
- Distribution-to-firewall Layer 3 design
- Management IP addresses for both switches
- Final use of VLAN 99
- Whether additional VLANs are required for future lab phases

Items that have not yet been architecturally decided should remain `TBD` rather than being configured arbitrarily.
