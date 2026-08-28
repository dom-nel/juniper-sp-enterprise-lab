# Google Cloud EVE-NG Deployment

## Purpose

This document records the migration of the EVE-NG platform from a local VMware Fusion environment to Google Cloud during Phase 1.

The migration provides a stable virtualization platform for the two vSRX nodes and the current endpoint topology while leaving room for later expansion.

## Why the Platform Changed

The original stack required one 16 GB Mac to run:

```text
macOS
└── VMware Fusion
    └── EVE-NG
        ├── LAB-FW-01 (vSRX)
        └── LAB-RTR-01 (vSRX)
```

The host memory and CPU were shared across every layer. Running both vSRX nodes produced instability and made it difficult to distinguish a network configuration problem from a virtualization resource problem.

The new access path is:

```text
Mac browser
└── Internet
    └── Google Cloud VM
        └── EVE-NG
            └── Virtual lab nodes
```

The Mac is now the client. Google Cloud supplies the compute resources used by EVE-NG and its nested virtual machines.

## Cloud Host Specification

| Resource | Deployed Value |
|---|---:|
| Operating system | Ubuntu Server 22.04 LTS |
| Virtual CPUs | 8 |
| Memory | 32 GB |
| Boot disk | 100 GB |
| Nested virtualization | Enabled |
| EVE-NG package | Community `6.2.0-4` |
| EVE-NG kernel | `6.7.5-eveng-6-ksm+` |

The repository intentionally omits the Google Cloud project ID, public IP address, account data, and credentials.

## Nested Virtualization Requirement

EVE-NG runs virtual network appliances inside the Google Cloud VM. The host must expose Intel VMX virtualization instructions and the KVM device to the guest operating system.

Validation commands:

```bash
grep -cw vmx /proc/cpuinfo
sudo apt-get install -y cpu-checker
kvm-ok
```

Successful validation showed:

- VMX flags available across all 16 logical processor entries exposed to the guest.
- `/dev/kvm` present.
- KVM acceleration available.

## Installation Summary

EVE-NG Community was installed on the Ubuntu host using the supported Jammy installation path. The installation added the EVE-NG package and its custom kernel.

After installation and package updates, the VM was rebooted into the EVE-NG kernel. The first-boot wizard configured the EVE root account, hostname, domain, DHCP addressing, time settings, and direct internet connection.

DHCP remains appropriate inside the VM because Google Cloud controls the internal interface address. Static addressing should be managed at the cloud platform layer rather than forced inside EVE-NG.

## Host-Key Change During Setup

The first-boot wizard regenerated the server SSH host keys. Cloud Shell still held the old key, so the next SSH connection correctly stopped with a remote-host-identification warning.

The displayed new fingerprint matched the fingerprint produced by the setup wizard. The obsolete record was removed from Cloud Shell's Google Compute known-hosts file, and the new key was accepted on reconnection.

This was an expected key lifecycle event—not evidence of a man-in-the-middle attack.

## Validation

The final checks were:

```bash
uname -r
dpkg -l eve-ng | grep '^ii'
sudo test -f /opt/ovf/.configured && echo "EVE setup complete"
sudo systemctl is-active apache2 mysql
```

Results confirmed:

- The EVE-NG kernel was running.
- EVE-NG Community `6.2.0-4` was installed.
- The setup-completion marker existed.
- Apache was active.
- MySQL was active.
- The EVE-NG login page was reachable from a normal browser.

See [GCP Host Validation](../../validation-outputs/phase-1/gcp-host-validation.txt) for the sanitized output.

## Daily Operating Procedure

### Start the Lab

1. Open Google Cloud Compute Engine.
2. Start the EVE-NG VM.
3. Wait for the VM to reach the running state.
4. Open the EVE-NG web interface using the VM's current external address.
5. Start only the lab nodes required for the session.

### Stop the Lab

1. Stop all lab nodes inside EVE-NG.
2. Confirm configurations are committed and saved.
3. Stop the Google Cloud VM from Compute Engine.
4. Confirm the VM reaches the terminated state.

Stopping the VM preserves its persistent disk and EVE-NG installation while stopping compute charges. Persistent-disk and external IPv4 charges may continue according to the Google Cloud billing model.

## Security and Repository Rules

- Change the default EVE-NG administrator password.
- Restrict web and SSH ingress to trusted source addresses whenever practical.
- Do not publish passwords, private keys, SSH fingerprints, project IDs, or public IP addresses.
- Do not commit Juniper or other vendor operating-system images.
- Do not perform an Ubuntu release upgrade unless the target release is supported by the installed EVE-NG version.
- Store only sanitized topology exports, configurations, validation output, and screenshots in GitHub.

## Current Result

The licensed vSRX image and four-node topology were subsequently deployed in the cloud EVE-NG environment. Both Juniper devices became accessible through the remote console path, and the `LAB-FW-01` Phase 1 interface, zone, and static-route baseline was validated and committed.

The remaining work is documented in the [Phase 1 build record](README.md): finish `LAB-RTR-01`, configure both endpoints, demonstrate the expected pre-policy denial, add a narrow ICMP permit, and validate the resulting SRX session.
