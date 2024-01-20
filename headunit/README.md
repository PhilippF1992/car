# Hardware

* [Raspberry pi 4 8gb](https://amzn.eu/d/0oIf1Fr)
  * [128Gb SD Card](https://amzn.eu/d/2Dl5bnE)
* [RS485 Modbus Relays](https://amzn.eu/d/8nXaCZ0)
* [RS485 HAT](https://amzn.eu/d/72dqG40)
* PCB (TempSensors/Dimm Leds)
  * [Mosfets](https://www.infineon.com/cms/de/product/power/mosfet/n-channel/irlb8721/) (to dimm Leds/Fans)
    * 1k Ohm Resistors
  * 4,7k Ohm Resistors (DS18B20)
  * Screw Terminals (to connect sensors & Leds/Fans + 12V Power + 5V Power)
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
Go To Interface Options > Serial Port
Answer first No and then answer Yes and press ok
Go TO Advanced Settings > Expand Filesystem
Go To Interface Options > I2C and answer Yes
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

### LEDs

Connect via Screwterminals to PCB

### Freshwater level sensor

Connect via Screwterminals to PCB

### Wastewater level sensor 

Connect via Screwterminals to PCB

### Temp Sensors

Connect via Screwterminals to PCB

## install Code 
Connect via SSH:

```sh
ssh user@car
```

```sh
git clone https://github.com/PhilippF1992/car.git
cd car
./setup.sh
```
change the opened filed to match your settings, like your mqtt pw

# Resources
[Multiple DS18B20](https://www.hackster.io/vinayyn/multiple-ds18b20-temp-sensors-interfacing-with-raspberry-pi-d8a6b0)