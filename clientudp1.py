import socket
import time

# Input IP & Port secara dinamis
server_ip = input("Masukkan IP Server:")
server_port = int(input("Masukkan Port Server:"))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

counter = 1
while True:
    pesan = input("Ketik pesan (atau 'exit' untuk berhenti): ")
    if pesan.lower() == "exit":
        client_socket.sendto(pesan.encode(), (server_ip, server_port))
        break
    
    pesan_full = f"{pesan}{counter}"
    client_socket.sendto(pesan_full.encode(), (server_ip, server_port))
    print(f"Dikirim: {pesan_full}")
    counter += 1
    
    time.sleep(1) 