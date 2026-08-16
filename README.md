# Juniper SP/Enterprise Lab

A portfolio-focused EVE-NG lab that models an enterprise network connected to a service-provider edge. The project combines Juniper routing and security, Arista switching, Linux services, troubleshooting, validation, and network automation.

## Current Status

**Phase 1 — Core Connectivity: In Progress**

The EVE-NG platform has been migrated from a resource-constrained local Mac environment to Google Cloud. The cloud host and EVE-NG services are validated. The four-node baseline topology still needs to be migrated, configured, and tested end to end before Phase 1 is complete.

## Baseline Traffic Path

```text
LAB-PC-01 → LAB-FW-01 → LAB-RTR-01 → LAB-PC-02
```

## Planned Expanded Path

```text
LAB-PC-01 → LAB-SW-01 → LAB-SW-02 → LAB-FW-01 → LAB-RTR-01 → LAB-PC-02
```

## Repository Structure

| Directory | Purpose |
|---|---|
| `topology/` | EVE-NG topology exports |
| `device-configs/` | Sanitized network-device configurations |
| `ubuntu-servers/` | Linux service configuration and notes |
| `automation/` | Python, PyEZ, Ansible, and validation automation |
| `validation-outputs/` | Evidence from commands and connectivity tests |
| `troubleshooting/` | Structured incident and root-cause records |
| `diagrams/` | Architecture diagrams and sanitized screenshots |
| `documentation/` | Design, addressing, roles, and phase records |

## Addressing Summary

| Function | Network |
|---|---|
| Enterprise VLANs | `10.10.0.0/16` |
| WAN and external testing | `10.20.0.0/16` |
| Transit and infrastructure | `10.255.0.0/16` |
| Loopbacks | `10.255.255.0/24` allocated as `/32` addresses |

## Documentation

- [Device Roles](documentation/device-roles.md)
- [Hostname Convention](documentation/hostname-convention.md)
- [Interface and Circuit Map](documentation/interface-circuit-map.md)
- [IP Addressing Plan](documentation/ip-addressing-plan.md)
- [VLAN Plan](documentation/vlan-plan.md)
- [Phase 1 Status](documentation/phase-1/README.md)
- [GCP EVE-NG Deployment](documentation/phase-1/gcp-eve-ng-deployment.md)
- [Local Resource Exhaustion](troubleshooting/local-vsrx-resource-exhaustion.md)
- [GCP Host Validation](validation-outputs/phase-1/gcp-host-validation.txt)

## Repository Safety

Licensed network operating-system images are not stored in this repository. Passwords, private keys, cloud project identifiers, public IP addresses, and other sensitive values must be removed from all published evidence.
