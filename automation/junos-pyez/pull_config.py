from getpass import getpass
from pathlib import Path
from jnpr.junos import Device

host = input("Router management IP: ").strip()
password = getpass("LAB-ADMIN password: ")

with Device(
    host=host,
    user="LAB-ADMIN",
    passwd=password,
    port=830,
    gather_facts=False,
) as router:
    reply = router.rpc.get_config(
        options={"database": "committed", "format": "set"}
    )
    config = "".join(reply.itertext()).strip() + "\n"

filename = Path(f"backup-{host}.set")
filename.write_text(config)
filename.chmod(0o600)
print(f"Configuration saved to {filename}")
