from machine import Pin

from webserver import init_network, start_server


def get_body(msg):
    return f"""<h1>ESP8266 Pins</h1>
            <p>The led is {msg}</p>
            """


led = Pin(33, Pin.OUT)


def handler(path):
    if path == "/on":
        led.on()
        return get_body("on")
    elif path == "/off":
        led.off()
        return get_body("off")


def run():
    init_network()
    start_server(handler)
