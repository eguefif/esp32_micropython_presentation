import button_interrupt
import button_interrupt_watchdog
from button import run as run_button
from server_led import run as run_led_example
from simple_led import run as run_simple_led

# run_simple_led()
# run_led_example(async_webserver=True)
# run_button()
button_interrupt_watchdog.run()
