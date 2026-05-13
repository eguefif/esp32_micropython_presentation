init:
  sudo uv run -m esptool -p /dev/ttyUSB0 erase-flash
  sudo uv run -m esptool -p /dev/ttyUSB0 --baud 460800 write-flash 0x1000 firmware.bin

simple-led:
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./simple_led.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :

server-led:
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./secret.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./webserver.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./async_webserver.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./server_led.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :main.py

button:
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./button.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :main.py

button-irq:
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./button_interrupt.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :main.py


cp:
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./secret.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./notify_user.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./webserver.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./async_webserver.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./server_led.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./button.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./button_interrupt.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./button_interrupt_watchdog.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./door_probe_interrupt.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./simple_led.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :

debug:
  sudo picocom -b 115200 /dev/ttyUSB0
