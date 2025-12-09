import socket
import time
import threading

username = input("Masukkan username: ")
socketClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketClient.connect(("172.30.2.114", 5002))

def send_messages():
    counter = 1
    while True:
        message = f"{username}: pesan ke-{counter}"
        socketClient.send(message.encode())
        print(f"Ter kirim: {message}")
        counter += 1
        time.sleep(1)

send_messages()