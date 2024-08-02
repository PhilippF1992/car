# Hardware


* [GL.iNet GL-AR300M16-Ext](https://amzn.eu/d/0dVSC5lE)
  * [Buckconverter](https://amzn.eu/d/btaRMiz)
* [LTE/Wifi/GPS Antenna](https://amzn.eu/d/gPD6HHo)
* [Netgear Aircard AC790](https://amzn.eu/d/8WNrSqS)
  * [USB Cable](https://amzn.eu/d/1h2yiqJ)
  * [SMA to TS9](https://amzn.eu/d/bAzYMrF)

# Setup

[Follow Setup of Router](https://docs.gl-inet.com/router/en/4/faq/first_time_setup/#for-models-that-have-wi-fi)

Connect Aircard via USB and setup tethering

[Setup Wireguard at Fritz.box](https://avm.de/service/vpn/wireguard-vpn-zur-fritzbox-am-computer-einrichten/)

Upload File as Wireguard Client to Router

Go to VPN-Dashboard and click on settings of wireguard client and allow access to LAN via VPN

Connect [Headunit](../headunit/README.md) via LAN-Kabel

At router GUI go to Network>Firewall and add portforwards to the [Headunit](../headunit/README.md):

For HomeAssistant via VPN: 

Name: HomeAssistant \
Protocol: TCP/UDP \
External Zone: wgclient \
External Port 8123 \
Internal Zone LAN \
Internal IP *Select Headunits IP* \
Internal Port 8123

For SSH access via VPN-Network: 

Name: SSH
Protocol: TCP/UDP \
External Zone: wgclient \
External Port 22 \
Internal Zone LAN \
Internal IP *Select Headunits IP* \
Internal Port 22 

