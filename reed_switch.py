import time

from machine import Pin, Timer

import notify_user
from webserver import init_network

pin = Pin(32, Pin.IN, Pin.PULL_DOWN)
timer = Timer(0)

# 0 => nothing
# 1 => pin interrupt triggered
# 2 => timer interrupt triggered
state = 0


def interrupt_handler(_p):
    global state
    state = 1


def timer_handler(_t):
    global state
    state = 2


def do_notify():
    print("Hey, the reed switch was trigger")
    try:
        notify_user.notify()
    except Exception as e:
        print(e)


def run():
    init_network()
    global state
    pin.irq(handler=interrupt_handler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
    print("Ready to check your door")
    while True:
        if state == 1:
            if pin.value() == 0:
                print("Schedule timer")
                timer.init(period=2_000, mode=Timer.ONE_SHOT, callback=timer_handler)
            else:
                print("Deinit timer")
                timer.deinit()
            state = 0
        if state == 2:
            timer.deinit()
            state = 0
            if pin.value() == 0:
                do_notify()
            else:
                print("Door was closed again.")
        time.sleep(0.2)
