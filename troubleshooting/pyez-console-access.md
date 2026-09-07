# Troubleshooting Record: PyEZ Could Not Reach the Cloud-Hosted vSRX Consoles

## Objective

Use one local Python program to connect to `LAB-FW-01` and `LAB-RTR-01` inside the EVE-NG lab hosted on Google Cloud and retrieve Junos device facts.

## Initial symptom

The vSRX nodes were usable from the EVE-NG environment, but attempting to treat their assigned console ports as directly reachable public services did not provide a reliable Python connection path.

## Working hypothesis

The failure was in the transport path to the console sockets, not proof that Junos, PyEZ, or the devices themselves were broken. EVE-NG had assigned console ports on the GCP VM, but a local process still needed a safe path to those host-local listeners.

## Isolation sequence

1. Confirmed the GCP VM was reachable through SSH.
2. Confirmed EVE-NG and both vSRX nodes were running.
3. Identified the EVE-NG console mappings:
   - `LAB-FW-01` -> TCP `32771`
   - `LAB-RTR-01` -> TCP `32772`
4. Verified that the GCP Linux host was listening on both ports.
5. Created two SSH local-forwarding rules in one authenticated SSH session.
6. Tested `127.0.0.1:32771` and `127.0.0.1:32772` from the workstation.
7. Pointed PyEZ at the local loopback address, selected each port from the Python inventory, and used `mode="telnet"` for the EVE-NG console session.
8. Retrieved device facts from both vSRX instances.

## Root cause

The Python process and the EVE-NG console sockets were on different hosts. A console port listening on the GCP VM is not automatically a safe or reachable local endpoint. The missing component was an explicit transport path from the workstation to those remote listeners.

## Resolution

SSH local port forwarding created that path:

```text
127.0.0.1:32771 -> SSH tunnel -> GCP VM 127.0.0.1:32771 -> LAB-FW-01 console
127.0.0.1:32772 -> SSH tunnel -> GCP VM 127.0.0.1:32772 -> LAB-RTR-01 console
```

The Python inventory then selected the correct local port for each logical device. PyEZ handled the Junos console login and returned structured facts.

## Why this worked

- The console services remained bound to the remote host rather than being exposed as open Internet services.
- SSH supplied encryption and authenticated access to the GCP VM.
- Local loopback bindings made the forwarded ports available only to processes on the workstation.
- PyEZ's Telnet console mode matched the service presented by EVE-NG.

## Validation

Success required more than an open TCP port. The final evidence showed:

- both inventory entries were attempted;
- both device sessions reported successful connections;
- each session returned a Junos hostname and model; and
- `LAB-RTR-01` returned additional live facts including Routing Engine state and Junos version.

See `validation-outputs/automation/pyez-facts-sanitized.txt`.

## Lessons retained

1. Troubleshoot the access stack in order: cloud VM, remote listener, SSH tunnel, local listener, authentication, application data.
2. An open port proves transport availability, not successful device authentication.
3. The next hop for a management connection can involve multiple layers even when the Python code points only to `127.0.0.1`.
4. Console access through an SSH tunnel is not the same as NETCONF over SSH.
5. Passwords, public addresses, project IDs, and private keys do not belong in repository evidence.
