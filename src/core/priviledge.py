import ctypes
import os
import platform
import sys

class PriviledgeMan:
    @staticmethod
    def check_admin() -> bool:
        try:
            return os.getuid==0 # Try Unix 
        except AttributeError:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0 # Windows 
    
    @staticmethod
    def request_admin() -> None:
        if platform.system() == "Windows":
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()

        else:
            os.execvp("sudo", ["sudo"] + sys.argv)

