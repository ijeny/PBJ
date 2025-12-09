import socket

kenthu = socket.SOCK_DGRAM
afan = socket.AF_INET
socketServer = socket.socket(afan, kenthu)

socketServer.bind(("172.30.2.114", 5000))
print("Server Mendengarkan....")

while True:
    clientData=socketServer.recvfrom(1024)
    addrs = clientData[1][0]
    msg = clientData[0].decode()
    print(addrs + " : " + msg)