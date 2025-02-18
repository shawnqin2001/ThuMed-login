import os
import requests
import zipfile
import tarfile
from pathlib import Path

class ClientInstaller:
    def __init__(self):
        self.install_path = {
            "Windows": Path("C:/Program Files/oc-client"),
            "Linux": Path("/usr/local/bin"),
            "Darwin": Path("/usr/local/bin")
        }
        self.oc_download_url = {
            "Windows" : "https://github.com/okd-project/okd/releases/download/4.7.0-0.okd-2021-09-19-013247/openshift-client-windows-4.7.0-0.okd-2021-09-19-013247.zip",
            "Linux" : "https://github.com/okd-project/okd/releases/download/4.7.0-0.okd-2021-09-19-013247/openshift-client-linux-4.7.0-0.okd-2021-09-19-013247.tar.gz",
            "Darwin" : {
                "arm64":
                "https://github.com/okd-project/okd/releases/download/4.15.0-0.okd-2024-03-10-010116/openshift-client-mac-arm64-4.15.0-0.okd-2024-03-10-010116.tar.gz",
                "x84_64":
                "https://github.com/okd-project/okd/releases/download/4.15.0-0.okd-2024-03-10-010116/openshift-client-mac-4.15.0-0.okd-2024-03-10-010116.tar.gz"
            }
        }
        self.helm_download_url = {
            "Windows" : "https://github.com/helm/helm/releases/download/v3.7.2/helm-v3.7.2-windows-amd64.zip",
            "Linux" : "https://github.com/helm/helm/releases/download/v3.7.2/helm-v3.7.2-linux-amd64.tar.gz",
            "Darwin" : {
            "arm64":"https://get.helm.sh/helm-v3.17.1-darwin-arm64.tar.gz",
            "x86_64":"https://get.helm.sh/helm-v3.17.1-darwin-amd64.tar.gz"}
        }


    def _download_file(self, url:str, save_path:Path) -> None:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

    def _add_path(self, path:Path, system:str) ->None:

        if system == "Windows":
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                'Environment',
                                0,
                                winreg.KEY_ALL_ACCESS)
            current_path = winreg.QueryValueEx(key, 'Path')[0]
            if str(path) not in current_path:
                winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ,
                                f"{current_path};{path}")
            winreg.CloseKey(key)
        else:
            shell_profile = Path.home() / ('.bashrc' if os.name != 'posix' else '.zshrc')
            with open(shell_profile, 'a') as f:
                f.write(f'\nexport PATH="{path}:$PATH"\n')

    def install_oc_client(self, system:str, arch="x86_64") -> None:
        url = self.oc_download_url[system]
        if system == "Darwin":
            url = url[arch]
        download_path = Path.home() / "Downloads" / url.split('/')[-1]
        print("Downloading packages", url)
        self._download_file(url, download_path)

        print("Installing oc")
        install_path = self.install_path[system]
        os.makedirs(install_path, exist_ok=True)

        if system == "Windows":
            with zipfile.ZipFile(download_path) as zip_file:
                zip_file.extractall(install_path)
        else:
            with tarfile.open(download_path) as tar_file:
                tar_file.extractall(install_path)

        print("Adding installation path to PATH")
        self._add_path(install_path, system)
        print("Installation complete")
