# Simple Led Example ---------------------------------------------
# from simple_led import run as run_simple_led
#
# run_simple_led()

# Network and Led Example ----------------------------------------

# from server_led import run as run_led_example

# run_led_example()
# run_led_example(async_webserver=True)


# Button Handling Example ----------------------------------------

# from button import run as run_button
#
# run_button()
from button_interrupt import run as run_button_irq

run_button_irq()

# Button Handling Example ----------------------------------------

# Watchdog Example ----------------------------------------

# import button_interrupt_watchdog
# button_interrupt_watchdog.run()
