# Hardware

* [Raspberry pi 4 8gb](https://amzn.eu/d/0oIf1Fr)
  * [128Gb SD Card](https://amzn.eu/d/2Dl5bnE)
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

Run scrupt directly 
```sh
wget -O - https://raw.githubusercontent.com/PhilippF1992/car/main/headunit/setup.sh | bash
```

or follow the steps below:

```sh
sudo apt update
sudo apt upgrade -y
sudo raspi-config
```

Go To Interface Options > Serial Port
Answer first No and then answer Yes and press ok
Go TO Advanced Options > Expand Filesystem
Go To Interface Options > I2C and answer Yes
Go to Finish and reboot


## Install Docker
From https://docs.docker.com/engine/install/debian/#install-using-the-repository


connect via SSH:
```sh
ssh user@car
```

### Add Docker's official GPG key:
```sh
mkdir /home/$USER/docker-volumes
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

### Add the repository to Apt sources:
```sh
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

### Install
```sh
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
### Set Permissions

```sh
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

## Setup HomeAssistant & Mqtt-Server(Mosquitto)

### HomeAssistant 
```sh
mkdir /home/$USER/docker-volumes/home-assistant
docker pull homeassistant/home-assistant:stable
docker run -d \
    --name homeassistant \
    --privileged \
    --restart=unless-stopped \
    -e TZ=Europe/Berlin \
    -v /home/$USER/docker-volumes/home-assistant:/config \
    --network=host \
    homeassistant/home-assistant:stable
nano /home/$USER/docker-volumes/home-assistant/configuration.yaml
```

write to add trusted proxies

where 10.253.0.1/24 are the ip-addresses of the vpn\
and 199.22.2.0/24 are the ip-addresses of your network in your car

    http:
      use_x_forwarded_for: true
      trusted_proxies:
        - 199.22.2.0/24
        - 10.253.0.1/24
and save via ctrl+x 


### Mosquitto
## Setup Mosquitto

```sh
docker pull eclipse-mosquitto
mkdir /home/$USER/docker-volumes/mosquitto
mkdir /home/$USER/docker-volumes/mosquitto/data
mkdir /home/$USER/docker-volumes/mosquitto/logs
mkdir /home/$USER/docker-volumes/mosquitto/config
nano /home/$USER/docker-volumes/mosquitto/config/mosquitto.conf
```
write

    persistence true
    persistence_location /mosquitto/data/
    log_dest file /mosquitto/logs/mosquitto.log
    listener 1883

    ## Authentication ##
    allow_anonymous true
    
and save via ctrl+x 

```sh
docker run -d \
        --name mosquitto \
        --restart=unless-stopped \
        -e TZ=Europe/Berlin \
        -v /home/$USER/docker-volumes/mosquitto:/mosquitto \
        -v /home/$USER/docker-volumes/mosquitto/data:/mosquitto/data \
        -v /home/$USER/docker-volumes/mosquitto/logs:/mosquitto/logs \
        --network=host \
        eclipse-mosquitto:latest

docker exec -it mosquitto sh -c "mosquitto_passwd -c /mosquitto/config/password.txt hass"

sudo nano /home/$USER/docker-volumes/mosquitto/config/mosquitto.conf
```
change

    ## Authentication ##
    allow_anonymous true

to 

    ## Authentication ##
    allow_anonymous false
    password_file /mosquitto/config/password.txt

and save via ctrl+x 

```sh
docker restart mosquitto
```

add mqtt to HomeAssistant with User and PW via the GUI of HA
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

[Victron Technical Documentation](https://www.victronenergy.com/support-and-downloads/technical-information)

[Automate raspi-config](https://raspberrypi.stackexchange.com/questions/28907/how-could-one-automate-the-raspbian-raspi-config-setup)