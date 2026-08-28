# Phase 1 Interface and Circuit Map

## Purpose

This document is the authoritative physical and logical connection map for the active four-node Phase 1 topology.

```text
LAB-PC-01 -> LAB-FW-01 -> LAB-RTR-01 -> LAB-PC-02
```

Switching, VLAN trunks, servers, and automation systems are not part of the active Phase 1 circuit map. They remain possible later expansions in the project roadmap.

## Circuit Map

| Circuit | Device A | Interface A | Device B | Interface B | Network | Purpose |
|---|---|---|---|---|---|---|
| `CKT-001` | LAB-PC-01 | `eth0` | LAB-FW-01 | `ge-0/0/0.0` | `10.10.10.0/24` | Enterprise endpoint LAN |
| `CKT-002` | LAB-FW-01 | `ge-0/0/1.0` | LAB-RTR-01 | `ge-0/0/0.0` | `10.255.0.0/30` | Firewall-router transit |
| `CKT-003` | LAB-RTR-01 | `ge-0/0/1.0` | LAB-PC-02 | `eth0` | `10.20.20.0/24` | WAN endpoint LAN |

## Device Interfaces

### LAB-PC-01

| Interface | Connected to | Address | Default gateway |
|---|---|---:|---:|
| `eth0` | LAB-FW-01 | `10.10.10.10/24` | `10.10.10.1` |

### LAB-FW-01

| Interface | Connected to | Address | Security role |
|---|---|---:|---|
| `ge-0/0/0.0` | LAB-PC-01 | `10.10.10.1/24` | `trust` zone and endpoint gateway |
| `ge-0/0/1.0` | LAB-RTR-01 | `10.255.0.1/30` | `untrust` zone and transit next-hop network |

### LAB-RTR-01

| Interface | Connected to | Address | Routing role |
|---|---|---:|---|
| `ge-0/0/0.0` | LAB-FW-01 | `10.255.0.2/30` | Firewall-facing transit |
| `ge-0/0/1.0` | LAB-PC-02 | `10.20.20.1/24` | WAN endpoint gateway |

### LAB-PC-02

| Interface | Connected to | Address | Default gateway |
|---|---|---:|---:|
| `eth0` | LAB-RTR-01 | `10.20.20.10/24` | `10.20.20.1` |

## Route Relationships

Directly connected interfaces on `CKT-002` use addresses from the same `/30`:

```text
10.255.0.0   network address
10.255.0.1   LAB-FW-01
10.255.0.2   LAB-RTR-01
10.255.0.3   broadcast address
```

The remote routes use the neighboring transit address as the next hop:

| Device | Destination | Next hop | Exit interface |
|---|---|---|---|
| LAB-FW-01 | `10.20.20.0/24` | `10.255.0.2` | `ge-0/0/1.0` |
| LAB-RTR-01 | `10.10.10.0/24` | `10.255.0.1` | `ge-0/0/0.0` |

## Troubleshooting Use

The map supports a hop-by-hop validation sequence:

1. Validate LAB-PC-01 to `10.10.10.1`.
2. Validate LAB-FW-01 to `10.255.0.2`.
3. Validate LAB-RTR-01 to `10.20.20.10`.
4. Validate both remote routes.
5. Validate the firewall's `trust -> untrust` policy context.
6. Test the complete path.

This avoids treating an end-to-end failure as one undifferentiated problem.

## Change Rule

When a link changes, update all of the following together:

- EVE-NG topology
- This circuit map
- IP addressing plan
- Device configurations
- Topology diagram
- Validation evidence

The expanded switching design will receive new circuit IDs only when it becomes an active implementation phase.
