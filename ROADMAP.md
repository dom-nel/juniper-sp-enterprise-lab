# Future Development Roadmap

This file contains planned work only. Nothing below should be described as implemented until configuration and validation evidence is committed to the repository.

## Phase 1 Closeout

- Finish LAB-RTR-01 and endpoint configuration.
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

## Phase 4 - Network Automation

- Enable NETCONF and establish Juniper PyEZ connectivity.
- Collect device facts and operational state.
- Compare current state with a known-good baseline.
- Add repeatable configuration and validation workflows under version control.

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
-> repeatable state collection
-> structured historical data
-> anomaly detection
-> machine-learning experimentation
```
