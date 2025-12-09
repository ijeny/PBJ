import socket
import threading
import sys
from datetime import datetime

host = '192.168.1.4'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} keluar!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print("Terhubung dengan {}".format(str(address)))
        
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        
        print("Username {}".format(nickname))
        broadcast("{} Bergabung!".format(nickname).encode('utf-8'))
        client.send('Terkoneksi dengan Server!'.encode('utf-8'))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
receive()