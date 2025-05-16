import socket

def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        # Attempt to connect to a well-known DNS server (Google)
        socket.setdefaulttimeout(timeout)
        with socket.create_connection((host, port)):
            return True
    except OSError:
        return False

if check_internet():
    print("Internet connection is active.")
else:
    print("No internet connection.")
