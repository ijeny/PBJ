import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", 5000))  # Bisa menerima dari semua IP

print("Server listening on port 5000...")

connected_clients = set()  # untuk menyimpan daftar client yang sudah connect

while True:
    data, addr = server_socket.recvfrom(1024)
    message = data.decode()

    # Jika client baru pertama kali mengirim pesan
    if addr not in connected_clients:
        connected_clients.add(addr)
        print(f"Client {addr[0]}:{addr[1]} connected.")

    print(f"{addr[0]}:{addr[1]} -> {message}")

    # Jika client mengirim 'exit', putuskan koneksi
    if message.lower() == "exit":
        print(f"Client {addr[0]} disconnected.")
        connected_clients.remove(addr)