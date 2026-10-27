# Juniper Networking Lab

A hands-on EVE-NG lab for building and troubleshooting a small Juniper network. The project combines routing and switching, a Linux test host, configuration backups with Python and Junos PyEZ, and documented validation. The initial vSRX lab was hosted on Google Cloud; a later two-router lab runs on a local Linux/EVE-NG host.

## Latest lab: switching, static routes and a Linux host

```mermaid
flowchart LR
    H["Hosts A-D"] --- S["LAB-SW-01-CLEAN"]
    S ---|"802.1Q trunk"| R1["LAB-RTR-01"]
    R1 ---|"10.255.0.0/30"| R2["LAB-RTR-02"]
    R2 ---|"10.20.20.0/24"| U["REMOTE-UBUNTU"]
```

![EVE-NG topology with a switch, two routers and a remote Ubuntu server](topology/two-router-lab-2026-10-27.png)

*EVE-NG topology snapshot from October 27, 2026. HOST-A through HOST-D connect to the lab switch. The switch connects to LAB-RTR-01, then LAB-RTR-02, with REMOTE-UBUNTU on the remote LAN. Both router management interfaces connect to MGMT.*

| Component | Role |
|---|---|
| `LAB-SW-01-CLEAN` | Virtual switch connecting the lab hosts to R1 |
| `LAB-RTR-01` (R1) | VLAN gateway and first routed hop |
| `LAB-RTR-02` (R2) | Transit router and gateway for the remote LAN |
| `REMOTE-UBUNTU` | Linux endpoint used for connectivity tests |
| `MGMT` | Separate management connectivity for the router `fxp0` interfaces |

The topology is a snapshot; the active configuration and results below are documented separately. The screenshot alone does not establish device configuration or end-to-end reachability.

## Static routing and validation

The lab uses a `10.255.0.0/30` transit network between R1 and R2. R1 has VLAN 10 and 20 gateway interfaces; R2 connects to the `10.20.20.0/24` remote LAN.

| Device | Destination | Observed next hop | Outgoing interface |
|---|---|---|---|
| R1 | `10.20.20.0/24` | `10.255.0.2` | `ge-0/0/1.0` |
| R2 | `10.10.10.0/24` | `10.255.0.1` | `ge-0/0/0.0` |

A Linux host test showed four successful pings to its local gateway, `10.20.20.1`. A separate R2-to-`10.10.10.10` test received only 8 of 26 replies; the loss needs further investigation. These results do not establish a clean end-to-end path across every VLAN.

- [Two-router static routing build record](documentation/static-routing/README.md)
- [Observed validation and screenshot evidence](validation-outputs/static-routing/README.md)

## Python and Junos PyEZ

I used Python, Junos PyEZ, and NETCONF over SSH to retrieve the committed configuration from `LAB-RTR-01` and save it locally in Junos `set` format. The saved script prompts for a management address and password. It reads configuration; it does not push changes.

- [Configuration backup script and run instructions](automation/junos-pyez/README.md)

## Earlier cloud-hosted vSRX lab

The original phase used a Google Cloud Compute Engine VM running Linux and EVE-NG to host Juniper vSRX appliances. It focused on IPv4 addressing, static routing, firewall zones, candidate configuration review, and route validation. Its firewall-policy and end-to-end acceptance tests remain documented as in progress.

- [Phase 1 build record](documentation/phase-1/README.md)
- [Phase 1 topology](topology/phase-1-topology.svg)
- [Google Cloud deployment](documentation/phase-1/gcp-eve-ng-deployment.md)
- [Resource-exhaustion troubleshooting](troubleshooting/local-vsrx-resource-exhaustion.md)

## Project files

| Path | Contents |
|---|---|
| `topology/` | EVE-NG topology export, diagrams, and topology screenshot |
| `documentation/` | Addressing, interfaces, deployment, and lab records |
| `validation-outputs/` | Command evidence and test notes |
| `automation/junos-pyez/` | Read-only configuration backup script |
| `troubleshooting/` | Fault isolation notes |
| `ROADMAP.md` | Earlier planned development; milestones are tracked in the individual build records |

Backups can contain authentication data and other sensitive settings. The repository omits full device backups, private credentials, and licensed appliance images.
