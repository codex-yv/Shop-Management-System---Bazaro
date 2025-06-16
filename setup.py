import subprocess
import sys
import socket

def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        # Attempt to connect to a well-known DNS server (Google)
        socket.setdefaulttimeout(timeout)
        with socket.create_connection((host, port)):
            return True
    except OSError:
        return False
# List of required third-party packages
if check_internet():
    required_packages = [
        "openpyxl",
        "pymongo",
        "pywin32",
        "python-dotenv",
        "pandas",
        "reportlab",
        "customtkinter"
    ]

    # Install each package using pip
    for package in required_packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
else:
    print("Please Connect to the internet!")
