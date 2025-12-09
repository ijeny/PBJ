import socket
from datetime import datetime
import threading

# socket untuk server 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("10.130.150.159", 12345))
print("Alamat IP: 10.130.150.159")

# menampilkan tanggal di bagian awal 
TanggalHari = datetime.now().strftime("%d-%m-%Y")
print("Tanggal hari in: ", TanggalHari)

name = input('Masukkan Username: ')
serverSocket.listen()
msg, addrs = serverSocket.accept()
print("Menerima koneksi dari ", addrs[0])
print('Connection Established. Terkoneksi dari: ',addrs[0])

client = (msg.recv(1024)).decode()
print(client + ' sudah terhubung.')

# mengirimkan nama server ke client
msg.send(name.encode())

# untuk menerima pesan dari client
def TerimaPesan():
    while True:
        message = msg.recv(1024).decode()
        if not message:
            break
        WaktuSekarang = datetime.now().strftime("%H:%M:%S")
        print(f"[{WaktuSekarang}] {client}: {message}")

# untuk mengirim pesan dari server ke client
def MengirimPesan():
    while True:
        pesan = input("Pesan dari client: ")
        waktu = datetime.now().strftime("%d-%m-%Y")
        msg.send(pesan.encode())
        print(f"[{waktu}] ({name}): {pesan}")

# menjalankan thread agar bisa kirim & terima secara bersama
threadTerima = threading.Thread(target=TerimaPesan)
threadKirim = threading.Thread(target=MengirimPesan)

threadTerima.start()
threadKirim.start()