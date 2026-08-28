# Hostname Convention

## Naming Standard

Device hostnames will follow this format:

`<SITE>-<ROLE>-<NUMBER>`

This naming convention provides a consistent way to identify where a device belongs, what function it performs, and its unique device number.

Examples:

- `LAB-FW-01`
- `LAB-RTR-01`
- `LAB-SW-01`
- `LAB-SW-02`
- `LAB-SRV-01`
- `LAB-PC-01`

## Naming Components

### SITE

The site identifies the environment or physical location where the device belongs.

For the current project:

- `LAB` = Juniper SP/Enterprise Lab environment

Additional site codes can be introduced later if the topology expands into multiple simulated locations.

### ROLE

The role identifies the primary function of the device.

| Code | Device Role |
|---|---|
| FW | Firewall |
| RTR | Router |
| SW | Switch |
| SRV | Server |
| PC | End Host |

### NUMBER

The number uniquely identifies devices that share the same role.

Device numbers use two digits.

Examples:

- `LAB-SW-01`
- `LAB-SW-02`
- `LAB-PC-01`
- `LAB-PC-02`

## Current Topology

The active Phase 1 topology is:

`PC-LAN -> FW-SRX -> RTR-SRX -> PC-WAN`

## Device Naming Map

| EVE-NG Name | Hostname | Role |
|---|---|---|
| PC-LAN | `LAB-PC-01` | Enterprise LAN client |
| FW-SRX | `LAB-FW-01` | Juniper SRX dedicated firewall |
| RTR-SRX | `LAB-RTR-01` | Juniper SRX operating in a routing-focused role |
| PC-WAN | `LAB-PC-02` | WAN-side / external test client |

## Naming Rules

- Use uppercase hostnames.
- Use hyphens between naming fields.
- Use two-digit device numbers.
- Hostnames identify device function rather than IP address.
- Devices performing different roles should receive hostnames that reflect those roles.
- Devices using the same hardware platform may still receive different role codes.

For example:

- `LAB-FW-01` and `LAB-RTR-01` are both Juniper SRX devices.
- `LAB-FW-01` identifies the SRX operating as the dedicated firewall.
- `LAB-RTR-01` identifies the SRX operating in the routing-focused role.

- Future switches will use the `SW` role code when the switching phase begins.

## Expansion Rule

New devices will follow the same naming standard as the topology grows.

Examples:

- A future access switch could become `LAB-SW-01`.
- An Ubuntu server could become `LAB-SRV-01`.
- An additional router could become `LAB-RTR-02`.

The hostname convention should remain stable so that device names are predictable throughout configurations, diagrams, validation outputs, and troubleshooting documentation.
