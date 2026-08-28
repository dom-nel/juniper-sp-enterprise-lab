# Phase 1 IP Addressing Plan

## Purpose

This document defines the active IPv4 plan for the four-node Phase 1 topology. It separates endpoint LANs from the infrastructure transit link and gives every routed interface a predictable address.

```text
LAB-PC-01 -> LAB-FW-01 -> LAB-RTR-01 -> LAB-PC-02
```

## Address Spaces by Function

| Address space | Current use |
|---|---|
| `10.10.0.0/16` | Enterprise-side networks |
| `10.20.0.0/16` | WAN and external test networks |
| `10.255.0.0/16` | Infrastructure and transit links |
| `10.255.255.0/24` | Reserved for future `/32` loopbacks |

Only the three Phase 1 networks below are active in the current design.

## Enterprise LAN

Network: `10.10.10.0/24`

| Address | Assignment |
|---|---|
| `10.10.10.0` | Network address |
| `10.10.10.1` | LAB-FW-01 trust-side interface and default gateway |
| `10.10.10.10` | LAB-PC-01 |
| `10.10.10.255` | Broadcast address |

A `/24` contains 256 total addresses and 254 traditional usable host addresses. That capacity supports a multi-device LAN; it does not imply that 254 devices are currently connected.

## Firewall-Router Transit

Network: `10.255.0.0/30`

| Address | Assignment |
|---|---|
| `10.255.0.0` | Network address |
| `10.255.0.1` | LAB-FW-01 untrust-side interface |
| `10.255.0.2` | LAB-RTR-01 firewall-facing interface |
| `10.255.0.3` | Broadcast address |

A `/30` contains four total addresses and two usable host addresses. It is intentionally sized for the two endpoints of this point-to-point routed link.

Both transit interfaces must use addresses from `10.255.0.0/30` so each device identifies the neighboring next hop as directly connected.

## WAN Endpoint LAN

Network: `10.20.20.0/24`

| Address | Assignment |
|---|---|
| `10.20.20.0` | Network address |
| `10.20.20.1` | LAB-RTR-01 WAN-facing interface and default gateway |
| `10.20.20.10` | LAB-PC-02 |
| `10.20.20.255` | Broadcast address |

## Device Addressing Matrix

| Device | Interface | Address | Default gateway or remote next hop |
|---|---|---|---|
| LAB-PC-01 | `eth0` | `10.10.10.10/24` | Default gateway `10.10.10.1` |
| LAB-FW-01 | `ge-0/0/0.0` | `10.10.10.1/24` | Directly connected enterprise LAN |
| LAB-FW-01 | `ge-0/0/1.0` | `10.255.0.1/30` | Route to WAN via `10.255.0.2` |
| LAB-RTR-01 | `ge-0/0/0.0` | `10.255.0.2/30` | Route to enterprise via `10.255.0.1` |
| LAB-RTR-01 | `ge-0/0/1.0` | `10.20.20.1/24` | Directly connected WAN LAN |
| LAB-PC-02 | `eth0` | `10.20.20.10/24` | Default gateway `10.20.20.1` |

## Routing Relationships

LAB-FW-01 is directly connected to:

- `10.10.10.0/24`
- `10.255.0.0/30`

It needs this remote route:

```text
10.20.20.0/24 -> next hop 10.255.0.2
```

LAB-RTR-01 is directly connected to:

- `10.255.0.0/30`
- `10.20.20.0/24`

It needs this return route:

```text
10.10.10.0/24 -> next hop 10.255.0.1
```

The remote next hops are usable because both live on the directly connected transit subnet.

## Reserved Future Addressing

The block `10.255.255.0/24` is reserved for future `/32` loopbacks and router IDs. No loopback should be described as active until it is configured and validated.

Additional enterprise VLANs and switching subnets will be assigned only when the switching phase begins. They are not part of the current Phase 1 implementation.

## Documentation Rules

- Record an address before configuring it.
- Keep the EVE-NG topology, circuit map, device configuration, and validation output synchronized.
- Distinguish planned addresses from configured addresses.
- Never infer the number of connected devices solely from a prefix length.
- Use the routing table to validate the selected next hop and exit interface.
