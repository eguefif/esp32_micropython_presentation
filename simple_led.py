import time

from machine import Pin


def run():
    led = Pin(33, Pin.OUT)
    while True:
        led.on()
        time.sleep(0.3)
        led.off()
        time.sleep(0.3)
