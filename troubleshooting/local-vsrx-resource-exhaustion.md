# Local vSRX Resource Exhaustion

## Incident Summary

The initial Phase 1 topology ran inside EVE-NG hosted by VMware Fusion on a 16 GB Mac. Operating two vSRX appliances at the same time caused instability that affected lab state and configuration work.

## Symptom

Observed behavior included:

- Severe host slowdown while both vSRX nodes were running.
- Inconsistent node behavior after restarts.
- Previously expected interfaces or routes no longer appearing.
- A router returning with an older rollback configuration.
- Difficulty determining whether failures belonged to Junos, EVE-NG, VMware Fusion, or the Mac host.

## Evidence

The local stack required memory and CPU for four layers:

```text
macOS → VMware Fusion → EVE-NG → two vSRX appliances
```

Each layer consumed resources before the virtual network appliances received their allocations. Running the second vSRX materially increased host pressure, while individual nodes and console access worked when the environment was less heavily loaded.

Junos rollback behavior also showed that the router had booted from saved configuration state rather than preserving the in-progress state expected during the session.

## Fault Domain

The fault domain was the local virtualization platform, not one isolated interface or routing statement.

Potential configuration errors still required normal Junos validation, but the host could not provide a sufficiently stable platform to trust every observed symptom as a network fault.

## Root Cause

The 16 GB Mac was oversubscribed. It had to support macOS, VMware Fusion, the EVE-NG guest, and two nested vSRX virtual machines simultaneously.

The problem was not simply that EVE-NG was virtual. The issue was the total resource demand across nested virtualization layers and the lack of dependable headroom.

## Resolution

The EVE-NG host was migrated to a Google Cloud VM with:

- 8 vCPUs
- 32 GB RAM
- 100 GB persistent disk
- Nested virtualization enabled
- KVM acceleration verified

The cloud EVE-NG installation and supporting services were validated before migrating the topology.

## Verification

Platform verification included:

```bash
grep -cw vmx /proc/cpuinfo
kvm-ok
uname -r
dpkg -l eve-ng
systemctl is-active apache2 mysql
```

The cloud host exposed virtualization extensions, provided `/dev/kvm`, booted the EVE-NG kernel, and ran both required application services.

## Lessons Learned

- Separate platform health from network configuration health.
- Validate the hypervisor before troubleshooting virtual appliances.
- Save and commit Junos configuration deliberately before restarting a node.
- Use `show system commit`, `show configuration | compare`, and rollback history when the active configuration is unexpected.
- Capture evidence before changing multiple fault domains.
- Size the lab for the complete nested stack, not only the appliance memory values.

## Preventive Actions

- Start only the nodes required for the current task.
- Monitor host CPU and memory during topology growth.
- Commit Junos changes at defined checkpoints.
- Export sanitized configurations after successful milestones.
- Stop the cloud VM when the lab is not in use.
- Reassess CPU and memory before adding multiple traffic generators or additional service nodes.
