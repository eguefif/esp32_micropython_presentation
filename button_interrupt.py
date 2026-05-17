import time

from machine import Pin

interrupt = False


def interrupt_handler(p):
    global interrupt
    if p.value() == 1:
        interrupt = True


def do_notify():
    print("Hey, the button was pushed")


def run():
    global interrupt
    pin = Pin(32, Pin.IN, Pin.PULL_DOWN)
    pin.irq(handler=interrupt_handler, trigger=Pin.IRQ_RISING)
    print("Listen to button")
    while True:
        if interrupt:
            do_notify()
            interrupt = False
        time.sleep_ms(10)
