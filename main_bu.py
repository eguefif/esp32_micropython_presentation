import socket
import time

import network
from machine import Pin


def get_body(msg):
    html = f"""<!DOCTYPE html>
    <html>
        <head> <title>ESP8266 Pins</title> </head>
        <body> <h1>ESP8266 Pins</h1>
            <p>The led is {msg}</p>
        </body>
    </html>
    """
    return html.encode()


led = Pin(33, Pin.OUT)


def send_ip(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.143", 8080))
    s.send(ip)
    s.close()


def init_network():
    print("Initializing network")
    sta_if = network.WLAN(network.WLAN.IF_STA)
    sta_if.active(True)
    sta_if.connect("Bbox-D1474EC5", "FdFPHtNZ76mvR1JDyN")
    while not sta_if.isconnected():
        time.sleep(1)
    # ip = sta_if.ipconfig("addr4")[0].encode()
    # print("Sending ip address")
    # send_ip(ip)


def handle_request(sock):
    while True:
        data += sock.recv(1024)
        if not data:
            break
    request = data.decode()
    first_line = request.split("\r\n")[0]
    path = first_line.split()[1]
    if path == "/on":
        led.on()
        return "on"
    elif path == "/off":
        led.off()
        return "off"


def start_server():
    s = socket.socket()
    s.bind(("0.0.0.0", 80))
    s.listen(1)

    print("listening on 0.0.0.0:80")
    try:
        while True:
            sock, addr = s.accept()
            print("client connected from", addr)
            msg = handle_request(sock)
            html = get_body(msg)
            header = f"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nContent-Length:{len(html)}\r\n\r\n"
            sock.send(header.encode())
            sock.send(html)
            time.sleep(2)
            sock.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Terminating")
        s.close()


init_network()
start_server()
