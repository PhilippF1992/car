# Hardware

* [Raspberry pi 4 8gb](https://amzn.eu/d/0oIf1Fr)
  * [128Gb SD Card](https://amzn.eu/d/2Dl5bnE)
* PCB (TempSensors/Dimm Leds)
  * [Mosfets](https://www.infineon.com/cms/de/product/power/mosfet/n-channel/irlb8721/) (to dimm Leds/Fans)
    * 1k Ohm Resistors
  * 3.3k Ohm Resistors (DS18B20)
  * [MCP27013]
  * [ADS1115](https://amzn.eu/d/c3uFTyn)
  

# Setup

Flash SD card with newsest Rasbian Lite (64-bit) Version
use Raspberry Pi Imager and enable Wifi + SSH

connect via SSH:
```sh
ssh user@car
```

Run scrupt directly 
```sh
wget -O - https://raw.githubusercontent.com/PhilippF1992/car/main/headunit/setup-rpi.sh | bash
```