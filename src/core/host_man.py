from pathlib import Path
from dataclasses import dataclass 
import platform
import ipaddress


@dataclass
class HostEntry:
    ip: str
    hostname: str

class HostManager:
    def __init__(self)-> None:
        self.host_path = {
            "Windows": Path("C:/Windows/System32/drivers/etc/hosts"),
            "Linux": Path("/etc/hosts"),
            "Darwin": Path("/etc/hosts")
        }[platform.system()]

    def validata_entry(self, entry:HostEntry)-> bool:
        try:
            ipaddress.ip_address(entry.ip)
            return all(c.isalnum() or c in ['-', '.'] for c in entry.hostname)
        except ValueError:
            return False 

    def add_entry(self, entry: HostEntry) -> None:
        if not self.validata_entry(entry):
            raise ValueError("Invalid hosts entry")

        entry_line = f"{entry.ip}\t{entry.hostname}"

        with open(self.host_path, "r+") as f:
            content = f.read()
            if entry_line not in content:
                f.write(f"\n{entry_line}\n")


    def generate_container_host(self, container_name:str) -> HostEntry:
        return HostEntry(
                ip = "166.111.153.65",
                hostname = f"{container_name}.apps.okd.med.thu"
                )








