import time

from machine import Pin, Timer

notify = False
pin = Pin(33, Pin.IN)
timer = Timer(0)
schedule_timer = False


def interrupt_handler(_p):
    global schedule_timer
    schedule_timer = True


def check_callback(_t):
    global notify
    timer.deinit()
    if pin.value() == True:
        notify = True


def do_notify():
    global notify
    notify = False
    print("Hey, the button was pushed")


def run():
    global schedule_timer
    pin.irq(handler=interrupt_handler, trigger=Pin.IRQ_RISING)
    while True:
        if schedule_timer:
            schedule_timer = False
            timer.init(period=2_000, mode=Timer.ONE_SHOT, callback=check_callback)
        if notify:
            do_notify()
        time.sleep(0.2)
