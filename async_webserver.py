import asyncio
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


async def get_path_from_request(reader):
    data = b""
    while True:
        data += await reader.read(1024)
        print(data)
        if not data or data[-4:] == b"\r\n\r\n":
            break
    request = data.decode()
    first_line = request.split("\r\n")[0]
    path = first_line.split()[1]
    return path


async def send_response(writer, body):
    header = f"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nContent-Length:{len(body)}\r\n\r\n"
    writer.write(header.encode())
    writer.write(body)
    await writer.drain()


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


async def send_404(writer):
    body = b"<h1>404 Not Found</h1>"
    header = f"HTTP/1.0 404 Not Found\r\nContent-Type: text/html\r\nContent-Length:{len(body)}\r\n\r\n"
    writer.write(header.encode())
    writer.write(body)
    await writer.drain()


async def handle_client(reader, writer, handler):
    info = reader.get_extra_info("peername")
    print("New client: ", info)
    try:
        path = await get_path_from_request(reader)
        body = handler(path)
        if not body:
            await send_404(writer)
        else:
            await send_response(writer, body)
        time.sleep(2)
    except Exception as e:
        print(f"Error: {e}")


async def start_server(host, port, handler):

    loop = asyncio.get_event_loop()

    client_handler = lambda reader, writer: handle_client(reader, writer, handler)
    server = asyncio.start_server(client_handler, host, port)
    loop.create_task(server)
    print("listening on 0.0.0.0:80")
    loop.run_forever()


def start_async_webserver(handler):
    asyncio.run(start_server("0.0.0.0", 80, handler))
