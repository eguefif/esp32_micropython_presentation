init:
  uv run -m esptool -p /dev/ttyUSB0 erase-flash
  uv run -m esptool -p /dev/ttyUSB0 --baud 460800 write-flash 0x1000 firmware.bin

simple-led:
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./simple_led.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :main.py

server-led:
  just web
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./server_led.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :main.py

button:
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./button.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :main.py

button-irq:
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./button_interrupt.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :main.py

reed-switch:
  just web
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./notify_user.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./reed_switch.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :main.py

web:
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./secret.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./webserver.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./async_webserver.py :


cp-all:
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./secret.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./notify_user.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./webserver.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./async_webserver.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./server_led.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./button.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./button_interrupt.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./button_interrupt_watchdog.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./door_probe_interrupt.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./simple_led.py :
  uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :

debug:
  picocom -b 115200 /dev/ttyUSB0
