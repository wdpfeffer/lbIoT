import time
import socket
import sys

sAddr = "192.168.1.201"

# connect to socket
def connect_socket(addr):
    s = socket.socket()
    print("Socket created")
    s.connect(addr)
    time.sleep(1)
    print("Socket connected")

    return s


def sendData(sData):
    # set socket address
    addr = socket.getaddrinfo(sAddr, 33733)[0][-1]
    try:
        s = connect_socket(addr)
        # make sure server is ready
        msg = s.recv(100).decode('utf-8')
        if msg == "ready":
            # do something
            s.send(sData.encode('utf-8'))
            s.close()

    except:
        print('exception occured', sys.exc_info()[0])
        # GoDeepSleep(5)