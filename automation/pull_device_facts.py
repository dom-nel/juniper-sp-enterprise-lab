"""Collect a small, sanitized fact set from Junos devices in the EVE-NG lab.

The EVE-NG console ports are bound to the remote GCP host. Before running this
script, forward those ports to the local workstation with SSH as documented in
automation/README.md.
"""

from getpass import getpass

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError


DEVICES = [
    {
        "lab_name": "LAB-FW-01",
        "host": "127.0.0.1",
        "console_port": 32771,
    },
    {
        "lab_name": "LAB-RTR-01",
        "host": "127.0.0.1",
        "console_port": 32772,
    },
]

FACT_KEYS = (
    "hostname",
    "model",
    "version",
    "master",
    "current_re",
    "serialnumber",
)


def collect_facts(device_record, username, password):
    """Open one console session and return selected read-only device facts."""
    with Device(
        host=device_record["host"],
        port=device_record["console_port"],
        user=username,
        passwd=password,
        mode="telnet",
        gather_facts=True,
    ) as junos_device:
        return {key: junos_device.facts.get(key) for key in FACT_KEYS}


def main():
    username = input("Junos username: ").strip()
    password = getpass("Junos password: ")

    for device_record in DEVICES:
        lab_name = device_record["lab_name"]
        console_port = device_record["console_port"]
        print(f"\n[{lab_name}] local console port {console_port}")

        try:
            facts = collect_facts(device_record, username, password)
        except ConnectError as error:
            print(f"connection: failed ({error.__class__.__name__})")
            continue

        print("connection: successful")
        for key, value in facts.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
