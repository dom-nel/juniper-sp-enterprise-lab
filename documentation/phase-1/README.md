# Phase 1 - Static Routing and Stateful Firewall Baseline

## Status

**In Progress - firewall baseline committed; router, endpoints, and traffic validation remain**

Phase 1 establishes controlled connectivity across the initial four-node topology:

```text
LAB-PC-01 -> LAB-FW-01 -> LAB-RTR-01 -> LAB-PC-02
```

The purpose is not only to make a ping succeed. The phase proves, in order, how addressing, directly connected networks, static routing, security-zone classification, security policy, and stateful session handling combine to create an end-to-end path.

## Phase 1 Design

| Segment | Prefix | Connected devices | Purpose |
|---|---|---|---|
| Enterprise LAN | `10.10.10.0/24` | LAB-PC-01 and LAB-FW-01 | Protected endpoint network |
| Firewall-router transit | `10.255.0.0/30` | LAB-FW-01 and LAB-RTR-01 | Two-device routed link |
| WAN endpoint LAN | `10.20.20.0/24` | LAB-RTR-01 and LAB-PC-02 | External test network |

| Device | Interface | Address | Role |
|---|---|---|---|
| `LAB-PC-01` | `eth0` | `10.10.10.10/24` | Enterprise endpoint |
| `LAB-FW-01` | `ge-0/0/0.0` | `10.10.10.1/24` | Trust-side gateway |
| `LAB-FW-01` | `ge-0/0/1.0` | `10.255.0.1/30` | Untrust-side transit |
| `LAB-RTR-01` | `ge-0/0/0.0` | `10.255.0.2/30` | Firewall-facing transit |
| `LAB-RTR-01` | `ge-0/0/1.0` | `10.20.20.1/24` | WAN-side gateway |
| `LAB-PC-02` | `eth0` | `10.20.20.10/24` | WAN endpoint |

## Platform Work Completed

- [x] Identified local nested-virtualization resource exhaustion.
- [x] Provisioned an Ubuntu 22.04 Compute Engine VM with 8 vCPUs, 32 GB memory, and a 100 GB boot disk.
- [x] Enabled and verified nested virtualization and KVM acceleration.
- [x] Installed EVE-NG Community and booted its custom kernel.
- [x] Configured administrative credentials and first-boot settings.
- [x] Verified Apache, MySQL, and browser access.
- [x] Deployed and accessed the Juniper vSRX nodes in cloud EVE-NG.
- [x] Managed the Linux host over SSH.
- [x] Used EVE-NG HTML5 access and Telnet device consoles.

## Firewall Baseline Completed

### Interface validation

The following output was verified on `LAB-FW-01`:

```text
ge-0/0/0                up    up
ge-0/0/0.0              up    up   inet     10.10.10.1/24
ge-0/0/1                up    up
ge-0/0/1.0              up    up   inet     10.255.0.1/30
```

**What this proves:** Both physical interfaces and logical units are operational, and the planned IPv4 addresses are active.

**What this does not prove:** Neighbor configuration, endpoint addressing, routing to the WAN network, security-zone assignment, policy authorization, or end-to-end connectivity.

### Existing-zone and policy inspection

The initial SRX configuration contained `trust` and `untrust` zone containers plus a broad `trust -> untrust` policy matching any source, destination, and application.

The interfaces were not initially assigned to the zones. The broad policy would have prevented a controlled demonstration of policy behavior because it could permit the test before a deliberate learning policy was added.

### Candidate firewall change

The candidate configuration:

- Assigned `ge-0/0/0.0` to `trust`.
- Assigned `ge-0/0/1.0` to `untrust`.
- Allowed host-inbound ping to each involved firewall interface.
- Removed the broad default `trust -> untrust` permit.
- Added a route to `10.20.20.0/24` through `10.255.0.2`.

Host-inbound ping permits ICMP addressed to the SRX itself. It does not authorize transit traffic passing through the firewall.

### Change-control validation

Before activation, the candidate was reviewed with:

```text
show | compare
```

It was then validated with:

```text
commit check
```

Junos returned:

```text
configuration check succeeds
```

The change was activated with the descriptive comment `Phase 1 firewall zones and static route baseline`.

### Active route validation

The firewall routing table returned:

```text
10.20.20.0/24      *[Static/5]
                    >  to 10.255.0.2 via ge-0/0/1.0
```

**What this proves:** `LAB-FW-01` has selected an active static route to the network containing `LAB-PC-02`. Matching traffic will use `LAB-RTR-01` at `10.255.0.2` as its next hop through `ge-0/0/1.0`.

**What this does not prove:** The router responds, its WAN interface is configured, the endpoint is reachable, or a security policy permits the flow.

## Why the Current Missing Policy Is Intentional

At this checkpoint:

```text
Interface state     = validated
Firewall addressing = validated
Zone assignment     = committed
Remote route        = active
Transit permit      = intentionally absent
```

This creates a controlled denial stage. After the router and endpoints are configured, the first end-to-end test should fail because no `trust -> untrust` policy authorizes it. A narrow ICMP policy will then be added so the change in behavior can be attributed to one controlled configuration change.

## Remaining Execution Steps

### LAB-RTR-01

- [ ] Confirm `ge-0/0/0.0` and `ge-0/0/1.0` survived the cloud migration.
- [ ] Configure `10.255.0.2/30` on the firewall-facing interface.
- [ ] Configure `10.20.20.1/24` on the WAN-facing interface.
- [ ] Configure the SRX for the intended routing-focused role.
- [ ] Add the return route `10.10.10.0/24 -> 10.255.0.1`.
- [ ] Run `show | compare`, `commit check`, and a descriptive commit.
- [ ] Verify the active return route.

### Endpoints

- [ ] Configure LAB-PC-01 as `10.10.10.10/24` with gateway `10.10.10.1`.
- [ ] Configure LAB-PC-02 as `10.20.20.10/24` with gateway `10.20.20.1`.
- [ ] Verify each endpoint can reach its local gateway.

### Controlled firewall tests

- [ ] Prove LAB-PC-01 cannot reach LAB-PC-02 without a transit permit.
- [ ] Record the expected failure.
- [ ] Add a narrow `trust -> untrust` ICMP policy.
- [ ] Review and commit the policy change.
- [ ] Prove LAB-PC-01 can reach LAB-PC-02.
- [ ] Verify the intended policy matches the traffic.
- [ ] Inspect the SRX session table and document forward and return flow handling.
- [ ] Initiate traffic from LAB-PC-02 and prove it remains denied without an `untrust -> trust` policy.

### Repository closeout

- [ ] Export sanitized final configurations.
- [ ] Save command output as text where practical.
- [ ] Add sanitized screenshots for important checkpoints.
- [ ] Confirm no credentials, public IP addresses, project identifiers, or vendor images are committed.
- [ ] Mark Phase 1 complete only after every acceptance criterion passes.

## Acceptance Criteria

| Test | Evidence | Required result |
|---|---|---|
| Firewall interfaces | `show interfaces terse` | Both interfaces `up/up` with planned addresses |
| Firewall zones | Zone configuration/output | LAN in `trust`; transit in `untrust` |
| Firewall route | `show route 10.20.20.0/24` | Active through `10.255.0.2` |
| Router interfaces | `show interfaces terse` | Both interfaces `up/up` with planned addresses |
| Router return route | `show route 10.10.10.0/24` | Active through `10.255.0.1` |
| Local reachability | Endpoint-to-gateway pings | Success on both LANs |
| Pre-policy transit | LAB-PC-01 to LAB-PC-02 | Expected failure |
| Post-policy transit | LAB-PC-01 to LAB-PC-02 | Success through intended policy |
| Stateful handling | SRX session output | Forward and return traffic in one permitted session |
| Reverse initiation | LAB-PC-02 toward LAB-PC-01 | Denied without reverse policy |

## Evidence Naming Standard

Use descriptive names under `validation-outputs/phase-1/`, for example:

```text
lab-fw-01-show-compare-pre-commit.png
lab-fw-01-commit-check-success.png
lab-fw-01-route-to-wan.txt
lab-rtr-01-route-to-enterprise.txt
pre-policy-ping-failure.txt
post-policy-ping-success.txt
srx-session-validation.txt
reverse-initiation-denied.txt
```

Each item should state what the evidence proves and what remains outside its scope.

## Related Records

- [Google Cloud EVE-NG Deployment](gcp-eve-ng-deployment.md)
- [Phase 1 Topology](../../topology/phase-1-topology.svg)
- [Interface and Circuit Map](../interface-circuit-map.md)
- [IP Addressing Plan](../ip-addressing-plan.md)
- [Local vSRX Resource Exhaustion](../../troubleshooting/local-vsrx-resource-exhaustion.md)
- [GCP Host Validation](../../validation-outputs/phase-1/gcp-host-validation.txt)
