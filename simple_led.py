import time

from machine import Pin


def run():
    led = Pin(33, Pin.OUT)

    print("Led on")
    led.on()
    time.sleep(2)
    led.off()
    print("Led off")
