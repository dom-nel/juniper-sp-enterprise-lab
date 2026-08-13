# Device Roles

## Architecture Overview

The baseline topology represents a simplified enterprise network connecting a protected LAN environment to an external/WAN network.

`PC-LAN → FW-SRX → RTR-SRX → PC-WAN`

## Device Role Mapping

| EVE-NG Device | Planned Hostname | Real-World Role |
|---|---|---|
| PC-LAN | `LAB-PC-01` | Enterprise user/client endpoint |
| FW-SRX | `LAB-FW-01` | Enterprise security edge firewall |
| RTR-SRX | `LAB-RTR-01` | WAN / service-provider edge router |
| PC-WAN | `LAB-PC-02` | External network / remote test endpoint |

## LAB-PC-01

Represents an internal enterprise endpoint.

### Purpose

- Generate traffic from the protected LAN
- Test default-gateway connectivity
- Test routing through the network
- Test firewall policies
- Validate end-to-end application connectivity

## LAB-FW-01

Represents the enterprise security boundary.

### Purpose

- Separate trusted LAN traffic from external networks
- Enforce security policies
- Perform stateful traffic inspection
- Route traffic between the enterprise LAN and upstream router
- Provide a realistic Juniper SRX security configuration target

## LAB-RTR-01

Represents the upstream WAN or service-provider edge router.

### Purpose

- Provide Layer 3 connectivity beyond the enterprise firewall
- Represent an ISP/provider-facing routing device
- Provide a foundation for future static routing, OSPF, and BGP labs
- Simulate upstream network reachability

## LAB-PC-02

Represents a host located outside the enterprise network.

### Purpose

- Simulate an external or remote endpoint
- Verify connectivity across the complete topology
- Generate return traffic toward the enterprise LAN
- Test firewall behavior from the outside network

## Traffic Flow

A basic end-to-end traffic flow follows:

`LAB-PC-01 → LAB-FW-01 → LAB-RTR-01 → LAB-PC-02`

This provides the initial architecture that will later expand to include switching, VLANs, servers, dynamic routing, automation, and additional service-provider components.
