
# Interface and Circuit Mapping

## Purpose

This document records how devices in the lab are physically and logically connected.

The interface and circuit map provides a single reference for:

- Which devices connect to each other
- Which interfaces are used
- What each connection is used for
- Which networks or VLANs cross each connection
- How individual links are identified during troubleshooting and validation

This document should be updated whenever the EVE-NG topology changes.

---

## Original Baseline Topology

The original Phase 0 topology was:

`PC-LAN → FW-SRX → RTR-SRX → PC-WAN`

The original EVE-NG `.unl` topology is preserved as the baseline version of the lab.

---

## Planned Topology

The planned topology expands the enterprise side of the network:

`PC-LAN → ACCESS-SW → DIST-SW → FW-SRX → RTR-SRX → PC-WAN`

The topology now contains the following architectural layers:

- Enterprise endpoint
- Access layer
- Distribution layer
- Security edge
- WAN/service-provider edge
- External endpoint

---

## Circuit Map

| Circuit ID | Device A | Interface A | Device B | Interface B | Network / Link Type | Purpose |
|---|---|---|---|---|---|---|
| CKT-001 | PC-LAN | `eth0` | ACCESS-SW | `TBD` | VLAN 10 / `10.10.10.0/24` | Enterprise endpoint access |
| CKT-002 | ACCESS-SW | `TBD` | DIST-SW | `TBD` | 802.1Q trunk | Access-to-distribution uplink |
| CKT-003 | DIST-SW | `TBD` | FW-SRX | `ge-0/0/0` | Layer 3 handoff - TBD | Enterprise-to-firewall connection |
| CKT-004 | FW-SRX | `ge-0/0/1` | RTR-SRX | `ge-0/0/0` | `10.255.0.0/30` | Firewall-to-router transit |
| CKT-005 | RTR-SRX | `ge-0/0/1` | PC-WAN | `eth0` | `10.20.20.0/24` | WAN-side test network |

> `TBD` interface values will be replaced after the Cisco switch platform and EVE-NG interface numbering are finalized.

---

## Device Interface Assignments

### LAB-PC-01

| Interface | Connected To | Purpose | Planned Network |
|---|---|---|---|
| `eth0` | LAB-SW-01 | Enterprise endpoint access | VLAN 10 / `10.10.10.0/24` |

---

### LAB-SW-01

`LAB-SW-01` represents the enterprise access-layer switch.

| Interface | Connected To | Purpose | Link Type |
|---|---|---|---|
| `TBD` | LAB-PC-01 | User access port | Access |
| `TBD` | LAB-SW-02 | Distribution uplink | 802.1Q trunk |

The exact Cisco interface numbers will be documented after the switch image is added to EVE-NG.

---

### LAB-SW-02

`LAB-SW-02` represents the enterprise distribution-layer switch.

| Interface | Connected To | Purpose | Link Type |
|---|---|---|---|
| `TBD` | LAB-SW-01 | Access-layer downlink | 802.1Q trunk |
| `TBD` | LAB-FW-01 | Security-edge uplink | Layer 3 handoff - TBD |

The distribution layer will eventually aggregate enterprise VLANs and may provide Layer 3 gateway functionality through SVIs/IRBs depending on the final design.

The exact Layer 3 boundary between the distribution switch and firewall will be finalized before configuration begins.

---

### LAB-FW-01

`LAB-FW-01` is the Juniper SRX operating as the dedicated enterprise firewall.

| Interface | Connected To | Purpose | Planned IP |
|---|---|---|---|
| `ge-0/0/0` | LAB-SW-02 | Enterprise / inside connection | TBD |
| `ge-0/0/1` | LAB-RTR-01 | WAN / outside transit | `10.255.0.1/30` |

The IP address on `ge-0/0/0` will be finalized after deciding where the enterprise VLAN default gateways and Layer 3 boundary will reside.

---

### LAB-RTR-01

`LAB-RTR-01` is the Juniper SRX operating in a routing-focused WAN/service-provider role.

| Interface | Connected To | Purpose | Planned IP |
|---|---|---|---|
| `ge-0/0/0` | LAB-FW-01 | Enterprise firewall transit | `10.255.0.2/30` |
| `ge-0/0/1` | LAB-PC-02 | WAN-side test network | `10.20.20.1/24` |

---

### LAB-PC-02

| Interface | Connected To | Purpose | Planned IP |
|---|---|---|---|
| `eth0` | LAB-RTR-01 | External/WAN endpoint | `10.20.20.10/24` |

---

## Circuit Naming Standard

Circuits use the following format:

`CKT-###`

Examples:

- `CKT-001`
- `CKT-002`
- `CKT-003`
- `CKT-004`
- `CKT-005`

Each circuit ID uniquely identifies a physical or logical connection in the lab.

Circuit IDs should remain stable whenever possible so that the same connection can be referenced consistently in:

- Documentation
- Diagrams
- Device configurations
- Validation outputs
- Troubleshooting notes
- Automation
- Change history

---

## Interface Documentation Rule

Whenever a new device or link is added to the topology:

1. Assign the connection a circuit ID.
2. Record both devices.
3. Record both interfaces.
4. Identify whether the connection is Layer 2 or Layer 3.
5. Record the associated VLANs or IP network.
6. Document the purpose of the connection.
7. Update the topology diagram.

This keeps the EVE-NG topology, documentation, and actual device configurations synchronized.

---

## Phase 0 Open Design Items

The following items must be finalized before configuration begins:

- Cisco access-switch platform
- Cisco distribution-switch platform
- Exact Cisco interface numbering
- VLANs allowed across the access-to-distribution trunk
- Layer 3 gateway placement for enterprise VLANs
- Distribution-to-firewall Layer 3 addressing
- Whether the distribution-to-firewall connection is a routed interface or another logical design

These items are intentionally marked as `TBD` rather than assigning values before the architecture decision is made.

