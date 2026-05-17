import time

from machine import Pin, Timer


def interrupt_handler(_p):
    global notify
    # if pin.value() == 1:
    notify = True


def do_notify():
    global notify
    print("Hey, the button was pushed")
    notify = False


pin = Pin(32, Pin.IN, Pin.PULL_DOWN)
pin.irq(handler=interrupt_handler, trigger=Pin.IRQ_RISING)
notify = False


def run():
    print("Listen to button")
    while True:
        if notify:
            do_notify()
        time.sleep(0.2)
