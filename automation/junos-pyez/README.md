# Junos Configuration Backup with Python and PyEZ

## Objective

Retrieve a router's committed configuration over NETCONF and save it locally in Junos `set` format. This is a read-only lab script; it does not load, change, or commit configuration.

## Observed lab result

In the October 22, 2026 session, I installed `junos-eznc` in a Python virtual environment, verified the PyEZ import, connected to `LAB-RTR-01`, and ran `pull_config.py`. The program reported a saved `backup-<management-ip>.set` file. The filename shown here replaces the home-lab management address with a placeholder. Inspection of the saved output showed the router hostname, SSH/NETCONF services, and VLAN 10/20 interface settings.

The script is recovered from the study record of that session. It preserves the lab username `LAB-ADMIN` used there; change it locally to the account configured on the target router. The example does not contain a password.

## Prerequisites

- Python 3 and `junos-eznc` installed in an isolated virtual environment.
- An authorized Junos device with a reachable management interface and NETCONF over SSH enabled.
- A working lab account and permission to retrieve the configuration.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python pull_config.py
```

Enter the device's current management IP when prompted, then enter the password without echoing it to the terminal. The script reads the committed configuration over TCP port 830, writes the returned text to a local file, and sets that file's permissions to `0600` after writing.

## Evidence and limits

The observed run established an authenticated, read-only retrieval and a local saved file. It did not modify a router, perform drift detection, or verify network traffic. Full backups may contain password hashes or other sensitive configuration, so generated `backup-*.set` files are ignored by Git and should remain private. The script is a learning example: it does not include production-grade exception handling or hardened file creation.
