import time

import network
from machine import Pin


def run():
    pin = Pin(33, Pin.IN, Pin.PULL_DOWN)
    print("Ready to listen for a button event")
    while True:
        if pin.value() == 1:
            print("Button down")
        time.sleep(0.2)
