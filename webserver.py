import socket
import time

import network

from secret import PASSWORD, SSID


# Setup the wifi
def init_network():
    print("Initializing network")
    sta_if = network.WLAN(network.WLAN.IF_STA)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        time.sleep(0.5)
    ip = sta_if.ipconfig("addr4")[0].encode()
    print("Device IP is: ", ip)


def get_path_from_request(sock):
    data = b""
    while True:
        data += sock.recv(1024)
        print(data)
        if not data or data[-4:] == b"\r\n\r\n":
            break
    request = data.decode()
    first_line = request.split("\r\n")[0]
    path = first_line.split()[1]
    return path


def send_response(sock, body):
    header = f"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nContent-Length:{len(body)}\r\n\r\n"
    sock.send(header.encode())
    sock.send(body)


def render_page(body):
    html = f"""<!DOCTYPE html>
    <html>
        <head> <title>ESP8266 Pins</title> </head>
        <body> 
        {body}
        </body>
    </html>
    """
    return html.encode()


def send_404(sock):
    body = b"<h1>404 Not Found</h1>"
    header = f"HTTP/1.0 404 Not Found\r\nContent-Type: text/html\r\nContent-Length:{len(body)}\r\n\r\n"
    sock.send(header.encode())
    sock.send(body)


def handle_client(sock, handler):
    path = get_path_from_request(sock)
    body = handler(path)
    if not body:
        send_404(sock)
    else:
        send_response(sock, body)
    time.sleep(2)
    sock.close()


def start_server(handler):
    s = socket.socket()
    s.bind(("0.0.0.0", 80))
    s.listen(1)

    print("listening on 0.0.0.0:80")
    while True:
        sock, addr = s.accept()
        print("client connected from", addr)
        try:
            handle_client(sock, handler)
        except Exception as e:
            print(f"Error: {e}")
            sock.close()
