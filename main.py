from server_led import run as run_led_example
from simple_led import run as run_simple_led

run_simple_led()
run_led_example(async_webserver=True)
