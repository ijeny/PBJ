import socket
import threading
import sys
from datetime import datetime

# Mengatur input() agar lebih bersih
userName = input("Masukkan username: ")

# Menggunakan IP lokal untuk koneksi (IP 192.168.1.4)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.4', 55555))

TanggalHari = datetime.now().strftime("%d-%m-%Y")
print("Tanggal hari ini: ", TanggalHari)

# PENTING: Cetak prompt awal '>> ' setelah info tanggal
sys.stdout.write('>> ')
sys.stdout.flush()

def receive():
    """Fungsi untuk menerima pesan dari server dan menampilkannya dengan rapi."""
    while True:
        try:
            # Menggunakan UTF-8 untuk mendukung karakter yang lebih luas
            message = client.recv(1024).decode('utf-8')
            
            if message == 'NICK':
                client.send(userName.encode('utf-8'))
            else:
                WaktuSekarang = datetime.now().strftime("%H:%M:%S")
                
                # 1. Hapus prompt '>> ' dan teks yang sedang diketik
                #    ('\r' kembali ke awal baris, ' ' * 80 membersihkan baris)
                sys.stdout.write('\r' + ' ' * 80 + '\r') 
                
                # 2. Cetak pesan yang diterima dengan format rapi
                sys.stdout.write(f"({WaktuSekarang})\n")
                sys.stdout.write(f"pesan: {message}\n")
                
                # 3. Cetak ulang prompt '>> ' agar input bisa dilanjutkan
                sys.stdout.write('>> ')
                sys.stdout.flush()

        except Exception as e:
            # Hapus prompt sebelum mencetak error
            sys.stdout.write('\r' + ' ' * 80 + '\r')
            print(f"Terjadi kesalahan! Koneksi terputus: {e}")
            client.close()
            break

def write():
    """Fungsi untuk mengirim pesan ke server."""
    while True:
        # Menggunakan input() tanpa prompt di dalamnya karena kita sudah mencetak '>> '
        # Ini akan menunggu input di baris yang sudah disediakan oleh sys.stdout.write di bawah.
        pesan_raw = input() 
        
        # Buat pesan lengkap untuk dikirim ke server
        message = '{}: {}'.format(userName, pesan_raw)
        
        WaktuSekarang = datetime.now().strftime("%H:%M:%S")
        
        # 1. Hapus baris yang baru saja digunakan oleh input()
        sys.stdout.write('\r' + ' ' * 80 + '\r') 
        
        # 2. Cetak pesan yang baru dikirim dengan format yang diinginkan
        sys.stdout.write(f"({WaktuSekarang})\n")
        sys.stdout.write(f"pesan: {message}\n")
        
        # 3. Cetak ulang prompt '>> ' untuk input berikutnya
        sys.stdout.write('>> ')
        sys.stdout.flush() 

        # Kirim pesan (menggunakan UTF-8)
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()