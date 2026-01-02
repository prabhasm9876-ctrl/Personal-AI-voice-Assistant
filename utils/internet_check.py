import socket

def has_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), 2)
        return True
    except:
        return False

