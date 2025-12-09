import socket
import threading
import time

socketClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
nomer = 0
socketClient.bind(("172.30.2.114", 5002))
print("Server menunggu...")

def func(number):
    x = socketClient.recvfrom(1024)
    addrs = x[1][0]
    msg = x[0].decode()
    no = str(number)
    print(f"[{addrs}] {msg}")

while True:
    nomer += 1
    t = threading.Thread(target=func, args=(nomer, ))
    t.start()