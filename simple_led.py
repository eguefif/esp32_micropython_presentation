import time

from machine import Pin


def light(led):
    print("Led on")
    led.on()
    time.sleep(2)
    led.off()
    print("Led off")


def run():
    led = Pin(33, Pin.OUT)
    # light(led)
    while True:
        led.on()
        time.sleep(0.3)
        led.off()
        time.sleep(0.3)
