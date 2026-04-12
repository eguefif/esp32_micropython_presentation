init:
  sudo uv run -m esptool -p /dev/ttyUSB0 flash-id

cp:
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./secret.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./webserver.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./led.py :
  sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp main.py :main.py

debug:
  sudo picocom -b 115200 /dev/ttyUSB0
