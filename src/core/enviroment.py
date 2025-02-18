import platform
import subprocess

class EnvironmentChecker:
    def __init__ (self):
        self.system = platform.system()
        self.helm_repo_url = "http://166.111.153.65:7001"

    def check_os_compatibility(self) -> bool:
        supported_os = ["Windows", "Linux", "Darwin"]
        return self.system in supported_os

    def check_oc_client(self) -> bool:
        try:
            result = subprocess.run(["oc", "version"], capture_output=True, text=True, check=True)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def check_helm_client(self) -> bool:
        try:
            result = subprocess.run(["helm", "version"], capture_output=True, text=True, check=True)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def check_helm_repo(self) -> bool:
        try:
            result = subprocess.run(["helm", "repo", "list"], capture_output=True, text=True, check=True)
            return self.helm_repo_url in result.stdout
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def full_enviromnment_check(self) -> dict:
        return {
            "os_compatibility": self.check_os_compatibility(),
            "oc_client": self.check_oc_client(),
            "helm_client": self.check_helm_client(),
            "helm_repo": self.check_helm_repo(),
            "system_info" :{
                "system:": self.system,
                "architecture:": platform.machine(),
                "release:": platform.release()
            }
        }
