#!/bin/sh
sudo apt update
sudo apt upgrade -y 
sudo apt install python3-rpi.gpio -y
sudo apt install python3-pip -y
sudo apt install python3-systemd -y 
sudo apt install python3-paho-mqtt -y
sudo apt install python3-serial -y
pip3 install ADS1x15-ADC --break-system-packages

sudo useradd -r -s /bin/false python_car
sudo adduser python_car gpio

sudo bash -c "echo 'dtoverlay=w1-gpio,gpiopin=3' >> /boot/config.txt"

sudo cp -r car/code /usr/local/lib/

sudo chown root:root /usr/local/lib/car/code/src/main.py

sudo chmod 644 /usr/local/lib/car/code/src/main.py

sudo cp /usr/local/lib/car/code/service/python_car.service /etc/systemd/system/python_car.service 