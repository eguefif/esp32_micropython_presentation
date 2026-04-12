# Micropython primer

## TODO

- [ ] Find how to not sudo all the time

## Hardware

* Esp32 wroom dev kitc
* breadboard
* one led
* one 220Ω
* two jumper wires male/male

See the picture.

## Flashing the firmware (Linux)

We can use `esptool` to flash the hardware. You can install this program in your project via `pip install esptool`.

The command to flash your esp32 is:

```bash
sudo uv run -m esptool -p /dev/ttyUSB0 flash-id
```

**-p** stands for port. On Linux, it will be the file used by the system to represernt the usb port.

There are two ways you can use to know that. You can do a `ls /dev/` and look at the file that is mostlikely the usb.
Or you can use `dmesg` and `grep` to see where the kernel has mounted the usb port with the command `dmesg | grep USB` after  you plugged the device. Here is an example output:
```bash
$ sudo dmsg | grep USB

[29241.401573] usb 1-1: New USB device found, idVendor=10c4, idProduct=ea60, bcdDevice= 1.00
[29241.401591] usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[29241.401594] usb 1-1: Product: CP2102N USB to UART Bridge Controller
[29241.406268] usb 1-1: cp210x converter now attached to ttyUSB0 <--------
```
According to this log, the usb port is in `/dev/ttyUSB0`.

## Activate a led

Talk about the repl, the file structure and how to send main.py via pyboard or webrepl.
You can open a repl using an app like `picocom` or `minicom`.

```bash
$ picocom -b 115200 /dev/ttyUSB0
```

`-b 115200` defines the Baud Per Seconde at which the computer must send data. It also tells us at which pace to read the incoming data. This is part of the serial data communication system. We need to know the rate at which to decode signals otherwise, we might read several time the same symbol or miss other. 
I did not find where to know that number. I guess this is the default configuration for the usb port on the devkit.

```python
>> from machine import Pin
>> led = Pin(33, Pin.OUT)
>> led.on()
>> led.off()
```

To execute picocom, type `C-aC-x`


## Copying files

After we flashed the hardware, there is a filesystem that we can use to store files. There are two important files in the filesystem:
* boot.py
* main.py

The file `boot.py` will be the first to ran by the runtime. Then, it is some kind of initializer scrip that we can change to run things. Then, the run time will be `main.py`.

### Copy a file
We can copy files to the file system using [pyboard.py](https://github.com/micropython/micropython/blob/master/tools/pyboard.py).
You will need to install `pip install pyserial`.

Then, if you want to copy a file, run the following command. I use uv, so it will look like:
```bash
$ sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :main.py
# Or, you can type the shorthand
$ sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :
```

### Use case

There is a very simple program in `simple_led.py`, let's use as a practice example.

```bash
$ sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp./simple_led.py:main.py
```
Then reboot the esp32 using the reboot button (the button on the red led side).

## Debugging

In our code, we print debug some information. If we don't do anything, we won't be able to see these debug print. The way to see then is to run `picocom -b 115200 /dev/ttyUSB0`. 
It's usefull to know that we cannot have two program using `/dev/ttyUSB0`. So if you're listening to this tty, you won't be able to use `pyboard.py` to copy files on the esp32.

## Activate the led remotely

In this example, we will setup a webserver on our esp32 and allow a remote user to turn on and off the led.

### Activating network

The esp32 allows two ways of using the wifi:
* Connect to an existing wifi.
* Run as a wifi point.

We will use the first one to connect to an existing Wifi point. 
See the code in `init_network`.

### Setup the webserver
