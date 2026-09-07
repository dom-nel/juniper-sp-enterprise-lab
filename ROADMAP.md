# Future Development Roadmap

This file separates completed milestones from planned work. Nothing under a future milestone should be described as implemented until configuration and validation evidence is committed to the repository.

## Completed Automation Foundation

- Used Python and Junos PyEZ to connect to both vSRX consoles.
- Mapped `LAB-FW-01` and `LAB-RTR-01` to their EVE-NG console ports in a Python inventory.
- Protected the workstation-to-GCP path with SSH local port forwarding.
- Retrieved and documented structured, read-only device facts from both devices.
- Sanitized credentials, cloud identifiers, public addressing, and sensitive output before publication.

This is console-based, read-only state collection. It is not NETCONF-over-SSH or configuration automation.

## Phase 1 Closeout

- Finish `LAB-RTR-01` and endpoint configuration.
- Demonstrate pre-policy denial and post-policy ICMP success.
- Validate stateful SRX session handling.
- Export sanitized configurations and command output.

## Phase 2 - Switching Fundamentals

- Add an access and distribution switching layer after the four-node baseline is stable.
- Implement VLANs and 802.1Q trunks.
- Decide and document the Layer 3 gateway boundary.
- Validate VLAN membership, trunking, and inter-VLAN routing.

## Phase 3 - Dynamic Routing

- Replace selected static routes with OSPF after the protocol is studied and the static baseline is understood.
- Validate adjacency formation, route learning, failure behavior, and recovery.
- Introduce BGP only after the underlying routing and addressing model is independently explainable.

## Phase 4 - Management-Plane Automation

- Configure reachable management addressing for the lab devices.
- Enable `system services netconf ssh` on the intended interfaces.
- Establish direct PyEZ NETCONF sessions over SSH, normally on TCP 830.
- Compare current state with a known-good baseline.
- Add repeatable configuration validation before attempting configuration changes.
- Add configuration workflows only after rollback and evidence requirements are defined.

## Phase 5 - Telemetry and Data Engineering

- Store structured interface, route, session, configuration-change, and availability data.
- Build a historical network-state dataset.
- Correlate network state with incident timestamps.

## Phase 6 - Anomaly Detection Research

- Define measurable abnormal-network behavior.
- Establish a non-ML baseline.
- Evaluate whether anomaly-detection or machine-learning methods improve detection quality.
- Document the dataset, target, evaluation method, and limitations.

The dependency order is deliberate:

```text
Working network
-> manual validation
-> repeatable read-only collection
-> management-plane automation
-> structured historical data
-> anomaly detection
-> machine-learning experimentation
```
