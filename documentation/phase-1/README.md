# Phase 1 — Core Connectivity

## Status

**In Progress**

Phase 1 establishes basic routed connectivity across the initial four-node topology:

```text
LAB-PC-01 → LAB-FW-01 → LAB-RTR-01 → LAB-PC-02
```

The cloud lab platform is ready. Phase 1 is not complete until the topology is running in cloud EVE-NG and end-to-end traffic is proven.

## Objectives

- Run the baseline topology on a stable EVE-NG platform.
- Configure the enterprise LAN, firewall-to-router transit, and WAN test network.
- Apply the minimum SRX zones and security policies required for controlled traffic.
- Install static routing for bidirectional reachability.
- Validate the complete path with command output and connectivity tests.
- Preserve sanitized configurations and evidence in GitHub.

## Completed

- [x] Defined device roles and hostname conventions.
- [x] Defined the baseline IP addressing plan.
- [x] Preserved the original EVE-NG topology export.
- [x] Booted and accessed both vSRX nodes in the local lab.
- [x] Confirmed Junos operation and console access.
- [x] Began configuring the firewall and router transit path.
- [x] Identified local host resource exhaustion as a stability risk.
- [x] Deployed EVE-NG Community to Google Cloud.
- [x] Verified nested virtualization and KVM acceleration.
- [x] Verified the EVE-NG kernel, package, setup marker, web server, and database.
- [x] Confirmed browser access to the cloud EVE-NG interface.

## Remaining

- [ ] Upload the licensed vSRX image directly to cloud EVE-NG.
- [ ] Import or rebuild the four-node baseline topology.
- [ ] Restore and verify both SRX configurations.
- [ ] Configure `LAB-RTR-01` WAN interface as `10.20.20.1/24`.
- [ ] Configure `LAB-PC-01` as `10.10.10.10/24`.
- [ ] Configure `LAB-PC-02` as `10.20.20.10/24`.
- [ ] Configure the required SRX security zones and policies.
- [ ] Add static routes for bidirectional reachability.
- [ ] Validate interfaces, routes, ARP/neighbor state, policies, ping, and traceroute.
- [ ] Export sanitized device configurations.
- [ ] Capture final validation evidence.
- [ ] Mark Phase 1 complete.

## Completion Criteria

Phase 1 will be complete only when all of the following are true:

1. All four baseline nodes run reliably in cloud EVE-NG.
2. Each interface uses the address defined in the addressing plan.
3. Both SRX devices contain the required routes.
4. The firewall permits only the traffic required for the test.
5. `LAB-PC-01` can reach `LAB-PC-02`.
6. Return traffic succeeds.
7. Configurations and validation output are saved in the repository.
8. Published evidence contains no credentials or cloud-specific sensitive values.

## Related Records

- [GCP EVE-NG Deployment](gcp-eve-ng-deployment.md)
- [Local vSRX Resource Exhaustion](../../troubleshooting/local-vsrx-resource-exhaustion.md)
- [GCP Host Validation](../../validation-outputs/phase-1/gcp-host-validation.txt)
