import socket
from datetime import datetime

clientSocket = socket.socket()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("127.0.0.1", 12345))
    client_ip_otomatis = s.getsockname()[0]
    s.close()
    print("Alamat IP Client (otomatis terdeteksi): ", client_ip_otomatis)
except Exception as e:
    print("Gagal mendeteksi IP otomatis: ", e)

hostname = socket.gethostname()
client_ip = socket.gethostbyname(hostname)
print("Alamat IP Client :", client_ip)

server_host = input("Masukkan alamat IP Server : ")
server_port = int(input("Masukkan Port Server : "))
name = input("Masukkan username : ")

clientSocket.connect((server_host, server_port))
clientSocket.send(name.encode())

server_name = clientSocket.recv(1024).decode()
print(server_name, "Telah bergabung....")

while True:
    message = input("pesan : ")
    clientSocket.send(message.encode())