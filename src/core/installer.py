import os
import requests
from pathlib import Path

class ClientInstaller:
    def __init__(self):
        self.install_dir = {
            "Windows": Path("C:/Program Files/oc-client"),
            "Linux": Path("/usr/local/bin"),
            "Darwin": Path("/usr/local/bin")
        }
        self.download_url = {
            "Windows" : "https://github.com/okd-project/okd/releases/download/4.7.0-0.okd-2021-09-19-013247/openshift-client-windows-4.7.0-0.okd-2021-09-19-013247.zip",
            "Linux" : "https://github.com/okd-project/okd/releases/download/4.7.0-0.okd-2021-09-19-013247/openshift-client-linux-4.7.0-0.okd-2021-09-19-013247.tar.gz",
            "Darwin" : "https://github.com/okd-project/okd/releases/download/4.7.0-0.okd-2021-09-19-013247/openshift-client-macos-4.7.0-0.okd-2021-09-19-013247.tar.gz"
        }


    def _download_file(self, url:str, save_path:Path) -> None:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

    def _
