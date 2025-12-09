import socket
import threading

# --- KONFIGURASI JARINGAN CLIENT ---
# GANTI DENGAN IP LOKAL KOMPUTER SERVER (HARUS SAMA DENGAN FILE server.py)
HOST = '127.0.0.1'
PORT = 5000

# Meminta nama pengguna
name = input("Masukkan Nama Anda: ")

# Inisialisasi Socket dan Koneksi ke Server
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
except Exception as e:
    print(f"Gagal terhubung ke server. Pastikan IP dan Port sudah benar dan server sudah berjalan.")
    print(f"Detail Error: {e}")
    exit()

# Fungsi untuk menerima pesan dari server
def receive():
    while True:
        try:
            # Menerima pesan
            message = client.recv(1024).decode('utf-8')
            
            # Protokol: Jika server meminta nama, kirim nama
            if message == 'NAME':
                client.send(name.encode('utf-8'))
            else:
                print(message)
        except:
            # Jika terjadi error (misal: server mati atau koneksi hilang)
            print("\nKesalahan koneksi! Server mungkin terputus.")
            client.close()
            break

# Fungsi untuk mengirim pesan ke server
def write():
    while True:
        try:
            # Input pesan dan format menjadi "Nama: Pesan"
            message_input = input("")
            message = f'{name}: {message_input}'
            client.send(message.encode('utf-8'))
        except EOFError:
            # Untuk menangani Ctrl+C atau input terputus
            print("\nBerhenti mengirim pesan.")
            client.close()
            break
        except Exception:
             # Untuk menangani ketika client mencoba mengirim pesan setelah koneksi terputus
             break

if __name__ == '__main__':
    # Memulai thread untuk menerima pesan (supaya tidak terblokir saat input)
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    # Memulai thread untuk mengirim pesan
    write_thread = threading.Thread(target=write)
    write_thread.start()