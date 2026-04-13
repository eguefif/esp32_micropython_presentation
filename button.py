import time

from machine import Pin


def run():
    pin = Pin(33, Pin.IN)
    while True:
        if pin.value() == True:
            print("pin true")
        time.sleep(0.2)
