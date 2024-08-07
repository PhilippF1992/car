#!/bin/sh

#update repos
echo 'Updating System: Start'
sudo apt update
sudo apt upgrade -y
echo 'Updating System: Done'

#setup raspi-config
echo 'Configure raspi-config: Start'
sudo raspi-config nonint do_expand_rootfs
sudo raspi-config nonint do_serial_hw 0
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_onewire 0
echo 'Configure raspi-config: Start'

#setup dtoverlays
echo 'Setup dtoverlays: Start'
sudo bash -c  "echo -en 'dtoverlay=w1-gpio,gpiopin=4' >> /boot/firmware/config.txt"
sudo bash -c  "echo -en 'dtoverlay=pwm-2chan' >> /boot/firmware/config.txt"
echo 'Setup dtoverlays: Done'

#add docker
echo 'Installing Docker: Start'
#add GPG Key
echo 'Adding GPG-Key: Start'
mkdir /home/$USER/docker-volumes
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo 'Adding GPG-Key: Done'
#add repository
echo 'Adding Docker Repository: Start'
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
echo 'Adding Docker Repository: Done'
#install docker
echo 'Installing Docker from Repository: Start'
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
echo 'Installing Docker from Repository: Done'
#permissions docker
echo 'Seting Permissions for Docker: Start'
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
echo 'Seting Permissions for Docker: Done'
echo 'Installing Docker: Done'

#HomeAssistant
echo 'Installing HomeAssistant: Start'
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
echo 'Waiting 30seconds for HA to finish'
sleep 10

sudo bash -c  "echo -en 'http:\n' >> /home/$USER/docker-volumes/home-assistant/configuration.yaml"
sudo bash -c  "echo -en '  use_x_forwarded_for: true\n' >> /home/$USER/docker-volumes/home-assistant/configuration.yaml"
sudo bash -c  "echo -en '  trusted_proxies:\n' >> /home/$USER/docker-volumes/home-assistant/configuration.yaml"
sudo bash -c  "echo -en '    - 199.22.2.0/24\n' >> /home/$USER/docker-volumes/home-assistant/configuration.yaml"
sudo bash -c  "echo -en '    - 10.253.0.1/24\n' >> /home/$USER/docker-volumes/home-assistant/configuration.yaml"
echo 'Installing HomeAssistant: Done'

#Mosquitto
echo 'Installing Mosquitto: Start'
docker pull eclipse-mosquitto
mkdir /home/$USER/docker-volumes/mosquitto
mkdir /home/$USER/docker-volumes/mosquitto/data
mkdir /home/$USER/docker-volumes/mosquitto/logs
mkdir /home/$USER/docker-volumes/mosquitto/config
touch /home/$USER/docker-volumes/mosquitto/config/mosquitto.conf

sudo bash -c  "echo -en 'persistence true\n' >> /home/$USER/docker-volumes/mosquitto/config/mosquitto.conf"
sudo bash -c  "echo -en 'persistence_location /mosquitto/data/\n' >> /home/$USER/docker-volumes/mosquitto/config/mosquitto.conf"
sudo bash -c  "echo -en 'log_dest file /mosquitto/logs/mosquitto.log\n' >> /home/$USER/docker-volumes/mosquitto/config/mosquitto.conf"
sudo bash -c  "echo -en 'listener 1883\n' >> /home/$USER/docker-volumes/mosquitto/config/mosquitto.conf"
sudo bash -c  "echo -en '\n' >> /home/$USER/docker-volumes/mosquitto/config/mosquitto.conf"
sudo bash -c  "echo -en '## Authentication ##\n' >> /home/$USER/docker-volumes/mosquitto/config/mosquitto.conf"
sudo bash -c  "echo -en 'allow_anonymous true\n' >> /home/$USER/docker-volumes/mosquitto/config/mosquitto.conf"


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

sudo sed -i 's/allow_anonymous true/allow_anonymous false/g' /home/$USER/docker-volumes/mosquitto/config/mosquitto.conf
sudo bash -c  "echo -en 'password_file /mosquitto/config/password.txt' >> /home/$USER/docker-volumes/mosquitto/config/mosquitto.conf"

docker restart mosquitto
echo 'Installing Mosquitto: Done'

#install python and setup permissions
echo 'Installing Python and Libraries: Start'
sudo apt install python3-pip -y
sudo apt install libsystemd-dev -y
sudo apt install python3-virtualenvwrapper -y
echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3' >> /home/$USER/.bashrc
echo 'export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv' >> /home/$USER/.bashrc
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> /home/$USER/.bashrc
mkvirtualenv car
pip install --upgrade pip
pip install cysystemd 
pip install paho-mqtt
pip install serial
pip install Adafruit-Blinka
pip install adafruit-circuitpython-mcp230xx
pip install adafruit-circuitpython-ads1x15
pip install adafruit-circuitpython-tlc59711
echo 'Installing Python and Libraries: Done'

echo 'Setup Service User: Start'
sudo useradd -r -s /bin/false python_car -G gpio,i2c,spi
echo 'Setup Service User: Done'

echo 'Setup Code: Start'
sudo apt install git -y
git clone https://github.com/PhilippF1992/car.git
echo 'Setup Code: Done'

sudo sed -i "s/\/usr\/bin\/python3/\/home\/$USER\/.virtualenvs\/car\/bin\/python/g" /home/$USER/car/code/service/python_car.service

##TODO Configure.py
echo 'Reboot'
sudo reboot