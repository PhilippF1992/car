# Hardware

* [Raspberry pi 4 8gb](https://amzn.eu/d/0oIf1Fr)
  * [Buckconverter](https://amzn.eu/d/8qV0JrC)
  * [128Gb SD Card](https://amzn.eu/d/2Dl5bnE)
* [RS485 Modbus Relays](https://amzn.eu/d/8nXaCZ0)
* [RS485 HAT](https://amzn.eu/d/72dqG40)
* PCB (TempSensors/Dimm Leds)
  * [Mosfets](https://www.infineon.com/cms/de/product/power/mosfet/n-channel/irlb8721/) (to dimm Leds/Fans)
    * 1k Ohm Resistors
  * 4,7k Ohm Resistors (DS18B20)
  * Screw Terminals (to connect sensors & Leds/Fans + 12V Power)
  * RPI Pin Headers (to connect as Hat)
  * [ADS1115](https://amzn.eu/d/c3uFTyn)
  

# Setup

Flash SD card with newsest Rasbian Lite (64-bit) Version
use Raspberry Pi Imager and enable Wifi + SSH

connect via SSH:
```sh
  ssh user@car
```

```sh
sudo apt update
sudo apt upgrade -y
sudo raspi config
```
Go To Interface Options>Serial Port
Answer first No and then answer Yes and press ok
Go TO Advanced Settings > Expand Filesystem
Reboot

## add Hardware

### Victron Multiplus 2

connect Multiplus 2 via MK3-to-USB-Adapter

### Victron SmartSolar MPPT 150/45

connect via VE.Direct-to-USB-Adapter

### Victron SmartShunt 500A

connect via VE.Direct-to-USB-Adapter

### Autoterm 4D

Connect via USB-Adapter

## install Code 
Connect via SSH:

```sh
ssh user@car
```

```sh
sudo apt update
sudo apt upgrade -y
sudo apt install git -y
sudo apt install python3-rpi.gpio -y
sudo apt install python3-pip -y
sudo apt install python3-systemd -y 
sudo pip3 install paho-mqtt

sudo useradd -r -s /bin/false python_car
sudo adduser python_car gpio
sudo bash -c "echo 'dtoverlay=w1-gpio,gpiopin=3' >> /boot/config.txt"
```

# Resources
[Multiple DS18B20](https://www.hackster.io/vinayyn/multiple-ds18b20-temp-sensors-interfacing-with-raspberry-pi-d8a6b0)