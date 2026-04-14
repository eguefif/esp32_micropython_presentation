# Micropython primer

## TODO

- [ ] Find how to not sudo all the time when working on /dev/ttyUSB0

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

**-p** stands for port. On Linux, it will be the file used by the system to represent the usb port.

There are two ways you can use to know that. You can do a `ls /dev/` and look at the file that is most likely the usb.
Or you can use `dmesg` and `grep` to see where the kernel has mounted the usb port with the command `dmesg | grep USB` after you plugged the device. Here is an example output:
```bash
$ sudo dmesg | grep USB

[29241.401573] usb 1-1: New USB device found, idVendor=10c4, idProduct=ea60, bcdDevice= 1.00
[29241.401591] usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[29241.401594] usb 1-1: Product: CP2102N USB to UART Bridge Controller
[29241.406268] usb 1-1: cp210x converter now attached to ttyUSB0 <--------
```
According to this log, the usb port is in `/dev/ttyUSB0`.

## Turn on and off a led

You can open a repl using an app like `picocom` or `minicom`.

```bash
$ picocom -b 115200 /dev/ttyUSB0
```

`-b 115200` defines the Baud Per Second at which the computer must send data. It also tells us at which pace to read the incoming data. This is part of the serial data communication system. We need to know the rate at which to decode signals; otherwise, we might read the same symbol several times or miss others.
I did not find where to know that number. I guess this is the default configuration for the usb port on the devkit.

```python
>> from machine import Pin
>> led = Pin(33, Pin.OUT)
>> led.on()
>> led.off()
```

To exit picocom, type `C-aC-x`


## Copying files

After we flashed the hardware, there is a filesystem that we can use to store files. There are two important files in the filesystem:
* boot.py
* main.py

The file `boot.py` will be the first to ran by the runtime. Then, it is some kind of initializer scrip that we can change to run things. Then, the run time will be `main.py`.

### Copy a file

We can copy files to the file system using [pyboard.py](https://github.com/micropython/micropython/blob/master/tools/pyboard.py).
You first will need to install the dependency `pip install pyserial`.

Then, if you want to copy a file, run the following command. I use uv, so it will look like:
```bash
$ sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :main.py
# Or, you can type the shorthand
$ sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./main.py :
```

### Turn on a led

There is a very simple program in `simple_led.py`, let's use as a practice example.

```bash
$ sudo uv run pyboard.py -d /dev/ttyUSB0 -f cp ./simple_led.py :main.py
```
Then reboot the esp32 using the reboot button (the button on the red led side). Here is a picture of how I plugged things on the breadboard:

PICTURE

We put a 220 Ω resistance between the led and the esp32 to diminish the current. The led does not offer enough resistance to be used by itself.
We plug the resistance with the GPIO 33 and the led with the GND. If it does not work, try to swap the led.

## Debugging

In our code, we print debug information. The way to see then is to run `picocom -b 115200 /dev/ttyUSB0`. 
Beware that we cannot have two program using `/dev/ttyUSB0`. So if you're listening to this tty, you won't be able to use `pyboard.py` to copy files on the esp32.
Try to run the previous program and you will see the debug information.

The most important command to know while running picocom is `C-aC-x`. It will exit the program. The `C-a` switches mode to Raw console and `C-x` is the command to exit raw terminal.

## Activate the led remotely

In this example, we will setup a webserver on our esp32 and allow a remote user to turn on and off the led.

### Activating network

The esp32 allows two ways of using the wifi:
* Connect to an existing wifi.
* Run as a wifi point.

We will use the first one to connect to an existing Wifi point. 
See the code in `init_network`.

### Setup the webserver

For this example, we will use two files:
* [server_led.py](./server_led.py)
* [webserver.py](./webserver.py)

The first file contains the logic to run the server and a dispatch function to give to the server.

THe second file is a very simple webserver that listen to a socket and handle new client via the `handle_client`. Both functions take a `handler` function passed by the caller. This function must returns bytes when a path is handled of a falsy value to trigger a 404.

There is also an async version of the webserver in [async_webserver.py](./async_webserver.py).

## Button: check button

- [ ] Take picture

## Notify system

You can install the notification system via the docker compose file.
We use [ntfy.sh](https://ntfy.sh) as a notification system. Before you can subscribe, we need to send a first notification to activate the feed.

```bash
$ curl -d "Hey" "http://localhost:8080/door-open"

{"id":"7HV6WuBWR1u2","time":1776107631,"expires":1776150831,"event":"message","topic":"door-open","message":"Hey"}
```
It will create a new feed named `door-open` to which you can subscribe.

You can type the following command to get your IP address on your local WIFI network:

```bash
$ ip addr | grep wlan0 -A 5 | grep "inet "

inet 192.168.1.143/24 brd 192.168.1.255 scope global dynamic noprefixroute wlan0

```

You can check the code in [notify_user.py](./notify_user.py). We only send a simple post request along with the host in the header. We also need to read the response as it can prevent ntfy from registering the notification.

## Reed switch

The code is in [door_probe_interrupt.py](./door_probe_interrupt.py). The only difference with the `button_interrupt.py` code is that we check the opposite signal. The reed switch, when the door is closed, is triggering a high signal to the GPIO pin. When the door is open, the signal falls low. If it lasts too long, we notify the user.

## Watchdog

The example is in [button_interrupt.py](./button_interrupt_watchdog.py). A watchdog is some kind of a timer that is reset anytime we feed it. If the program fails to notify the watchdog, it will reset the system.

A way to simulate that is to add a firewall rule to the port 8080. Doing so will make the esp32 hang when trying to notify the user. As the OS silently drops the packet, the esp32 waits for the TCP handshake to happen. We can set a watchdog that will reset the system and avoid waiting.

Here is how to set the firewall:

```bash
sudo ufw deny 8080/tcp

# Then, when we want to drop the rule
sudo ufw allow 8080/tcp
```
