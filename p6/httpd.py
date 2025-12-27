import socket
import os
import mimetypes
from template import Template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def tcp_server():
    HOST = '127.0.0.1'
    PORT = 8080

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on http://{HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        request = client.recv(4096).decode()

        if request:
            response = handle_request(request)
            client.sendall(response)

        client.close()


def handle_request(request):
    lines = request.split("\r\n")
    method, uri, http_version = lines[0].split()

    if method == "GET":
        return handle_get(uri, http_version)

    if method == "POST":
        data = lines[-1]
        return handle_post(uri, http_version, data)

    return b""


def handle_get(uri, http_version):
    filename = "index.html" if uri == "/" else uri.lstrip("/")
    filepath = os.path.join(BASE_DIR, filename)

    if not os.path.isfile(filepath):
        return response_404()

    if filename.endswith(".html"):
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()

        content = Template(html).render({}).encode()
        content_type = "text/html"
    else:
        with open(filepath, "rb") as f:
            content = f.read()
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    return response_200(http_version, content, content_type)


def handle_post(uri, http_version, data):
    filename = uri.lstrip("/")
    filepath = os.path.join(BASE_DIR, filename)

    if not os.path.isfile(filepath):
        return response_404()

    _POST = {}
    for item in data.split("&"):
        if "=" in item:
            k, v = item.split("=", 1)
            _POST[k] = v

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    content = Template(html).render({"_POST": _POST}).encode()
    return response_200(http_version, content, "text/html")


def response_200(http_version, body, content_type):
    header = (
        f"{http_version} 200 OK\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
    ).encode()
    return header + body


def response_404():
    body = b"<h1>404 Not Found</h1>"
    header = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
    ).encode()
    return header + body


if __name__ == "__main__":
    tcp_server()