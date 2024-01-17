# Hardware

* [Raspberry Pi 4 4gb](https://amzn.eu/d/iuI6WAu)
  * [Buckconverter](https://amzn.eu/d/8qV0JrC)
  * [128Gb SD Card](https://amzn.eu/d/2Dl5bnE)
* [Wlan Sticks](https://amzn.eu/d/j6AgZBr)
* [LTE/Wifi/GPS Antenna](https://amzn.eu/d/gPD6HHo)
* [Netgear Aircard AC790](https://amzn.eu/d/8WNrSqS)
  * [USB Cable](https://amzn.eu/d/1h2yiqJ)
  * [SMA to TS9](https://amzn.eu/d/bAzYMrF)

# Setup

## Prepare 

### Basic Setup
Flash [newest Version](https://openwrt.org/toh/raspberry_pi_foundation/raspberry_pi)

connect RPI4 via Network-Cable directly to PC

Open Browser and go to 192.168.1.1 and login with root and empty password

Follow prompt to set password

Navigate to Network>Wireless

Scan for Networks and connect to Present Network

Navigate to Interfaces and edit Lan and change IPv4 address to 199.22.2.1

Reconnect Wired Connection and go to 199.22.2.1

### Resize storage on sd-card
From [guide](https://openwrt.org/docs/guide-user/advanced/expand_root):

connect via ssh:

```sh
ssh root@199.22.2.1
```
run:
```sh
opkg update
opkg install parted losetup resize2fs
wget -U "" -O expand-root.sh "https://openwrt.org/_export/code/docs/guide-user/advanced/expand_root?codeblock=0" . 
sh ./expand-root.sh
sh /etc/uci-defaults/70-rootpt-resize
reboot
```

## Enable Aircard
connect via ssh:

```sh
ssh root@199.22.2.1
```

install packages
```sh
opkg update
opkg install kmod-usb-net-rndis aircard-pcmcia-firmware
reboot
```

Aircard enable tethering and connect via USB-cable

Navigate to Network > Interfaces

Click the Add button

* Name: Aircard
* Protocol DHCP Client
* Device eth1

Firewall add to WAN

## Setup Wifi-Sticks
connect via ssh:

```sh
ssh root@199.22.2.1
```

install packages
```sh
opkg update
opkg install kmod-mt76-usb kmod-mt76x2u
reboot
```
Connect first wifi-stick

Navigate to Network>Wireless

Create wifi with name and password. 

Connect 2nd wifi-stick 
Connect to existing wifi if possible 
Disconnect wifi-access from 'Prepare' section

## Install and setup Failover Wifi>LTE
connect via ssh:

```sh
ssh root@199.22.2.1
```

install packages
```sh
opkg update
opkg install luci-app-mwan3 mwan3 iptables-nft iptables-nft
```

Navigate to Network>multiwan>interface

* Delete present interfaces
* Add interface for existing wans (wwan, Aircard)
  * Server:
    * 8.8.8.8
    * 8.8.4.4
    * 1.1.1.1
    * 1.0.0.1

Go to member
* Delete existing members
* Add member for existing wans (lower metric and weight are prefered over higher)
  * wwan_m5_w3
  * Aircard_m10_w3

Go to policy
* Delete exisiting policies
* Add policy for failover
  * name: failover 
  * add both member into policy

Go to rules
* Delete https rule
* Edit ipv4 and ipv6 rules, set sticky and choose created policy

## Install Docker
connect via ssh:

```sh
ssh root@199.22.2.1
```

run
```sh
opkg update
opkg install dockerd docker docker-compose nano luci-app-dockerman
mkdir /root/docker-volumes
reboot
```

## Setup Homeassistant
connect via ssh:

```sh
ssh root@199.22.2.1
```

```sh
mkdir /root/docker-volumes/home-assistant
docker pull homeassistant/home-assistant:stable
docker run -d \
    --name homeassistant \
    --privileged \
    --restart=unless-stopped \
    -e TZ=Europe/Berlin \
    -v /root/docker-volumes/home-assistant:/config \
    --network=host \
    homeassistant/home-assistant:stable
nano /root/docker-volumes/home-assistant/configuration.yaml
```
write to add trusted proxies

    http:
      use_x_forwarded_for: true
      trusted_proxies:
        - 199.22.2.0/24
        - 10.253.0.1/24

where 10.253.0.1/24 are the ip-addresses of the vpn

## Setup Mosquitto
connect via ssh:

```sh
ssh root@199.22.2.1
```

```sh
docker pull eclipse-mosquitto
mkdir /root/docker-volumes/mosquitto
mkdir /root/docker-volumes/mosquitto/data
mkdir /root/docker-volumes/mosquitto/logs
mkdir /root/docker-volumes/mosquitto/config
nano /root/docker-volumes/mosquitto/config/mosquitto.conf
```
write

    persistence true
    persistence_location /mosquitto/data/
    log_dest file /mosquitto/logs/mosquitto.log
    listener 1883

    ## Authentication ##
    allow_anonymous true

```sh
docker run -d \
        --name mosquitto \
        --restart=unless-stopped \
        -e TZ=Europe/Berlin \
        -v /root/docker-volumes/mosquitto:/mosquitto \
        -v /root/docker-volumes/mosquitto/data:/mosquitto/data \
        -v /root/docker-volumes/mosquitto/logs:/mosquitto/logs \
        --network=host \
        eclipse-mosquitto:latest

docker exec -it mosquitto sh -c "mosquitto_passwd -c /mosquitto/config/password.txt hass"

nano /root/docker-volumes/mosquitto/config/mosquitto.conf
```
change

    ## Authentication ##
    allow_anonymous true

to 

    ## Authentication ##
    allow_anonymous false
    password_file /mosquitto/config/password.txt

```sh
docker restart mosquitto
```

add mqtt to HomeAssistant with User and PW

## Install and setup Wireguard Client (Unraid HomeServer)
connect via ssh:

```sh
ssh root@199.22.2.1
```

install packages
```sh
opkg update
opkg install wireguard-tools luci-proto-wireguard
```

Navigate to Network>Interface

Add new interface and enter the following configuration:
* Name - give it any name, e.g. HomeVPNClient
* Protocol - WireGuard VPN

In the General Settings tab:

* Bring up on boot - Checked
* Private Key - generate keys

Go To unraid>Settings>VPN Manager

Peer Type: Access To LAN

Insert Peer Keys gerenated in OpenWRT

Click Apply

Click Eye Symbol and copy Interface>Address to OpenWRT IP Addresses
    
In Advanded Settings Tab:
* remove check at use default gateway

Go to Peers in OpenWRT and add Peer:
* Public Key - the WireGuard server public key (Unraid Eye Symbol in VPN Manager)
* Allowed IPs - (Unraid Eye Symbol in VPN Manager)
* Route Allowed IPs - Checked
* Endpoint Host - DDNS from Server
* Endpoint Port - 51820
* Keep Alive - 25

Click Save and Save&Apply
    
Navigate to System>Scheduled Jobs

Add Cronjob:
```sh
*/1 * * * * /usr/bin/wireguard_watchdog
*/10 * * * * ifdown HomeVPNClient && ifup HomeVPNClient
```

Navigate to Network - Firewall

Click the Add button and enter the following configuration:
* Name - Give it any name, e.g. VPN
* Input - Accept
* Output - Accept
* Forward - Accept
* Masquerading - Checked
* MSS clamping - Checked
* Covered networks - select the previously created VPN tunnel interface
* Allow forward to destination zones - lan,docker
* Allow forward from source zones - lan,docker
