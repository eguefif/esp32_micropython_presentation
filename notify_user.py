import socket


def notify():
    print("Notifying user")
    sock = socket.socket()
    host = "10.186.111.114"
    port = 8080
    topic = "door-open"
    message = b"Your door is open!!"

    sock.connect((host, port))

    header = (
        f"POST /{topic} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Content-Length: {len(message)}\r\n"
        f"Content-Type: text/plain\r\n"
        f"\r\n"
    ).encode()

    sock.send(header)
    sock.send(message)
    print("Notification sent")
    response = sock.recv(1024)
    print("Response:", response)

    sock.close()
    print("Done")
