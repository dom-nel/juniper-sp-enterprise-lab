# GCP-to-EVE-NG-to-vSRX Automation Path

```mermaid
flowchart LR
    subgraph LOCAL["Local workstation"]
        PY["Python 3<br/>Junos PyEZ"]
        LP1["127.0.0.1:32771"]
        LP2["127.0.0.1:32772"]
        PY --> LP1
        PY --> LP2
    end

    SSH["SSH local port forwarding<br/>encrypted across the Internet"]

    subgraph GCP["Google Cloud Compute Engine VM"]
        HOST["Linux host"]
        EVE["EVE-NG"]
        CP1["Console socket 32771"]
        CP2["Console socket 32772"]
        FW["LAB-FW-01<br/>Junos vSRX"]
        RTR["LAB-RTR-01<br/>Junos vSRX"]
        HOST --> EVE
        EVE --> CP1 --> FW
        EVE --> CP2 --> RTR
    end

    LP1 --> SSH --> CP1
    LP2 --> SSH --> CP2
```

## Protocol boundaries

| Segment | Protocol | Meaning |
|---|---|---|
| Workstation to GCP VM | SSH | Encrypts and authenticates the remote-host connection. |
| Local ports to remote ports | SSH local forwarding | Carries the two console TCP streams through the encrypted session. |
| PyEZ to Junos console prompt | Telnet-style console mode | Logs in to Junos and retrieves facts through the forwarded EVE-NG console socket. |

The word **Telnet** describes PyEZ's device-side console mode. The Internet-facing leg is inside SSH. No public console-port address is required or documented.

This diagram describes the management path used by the Python collector. It is separate from the Phase 1 data-plane topology in `topology/phase-1-topology.svg`.
