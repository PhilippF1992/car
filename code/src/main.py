import time
import argparse
import systemd.daemon
import paho.mqtt.client as mqtt
from classes.device import *
from classes.watersystem import *

parser = argparse.ArgumentParser(description='Controll your Car via MQTT and HA')
parser.add_argument('-mqttuser', dest='mqtt_user', type=str, default="hass",
                    help="MQTT Username (Default: hass)")
parser.add_argument('-mqttpw', dest='mqtt_password', type=str, default="",
                    help="MQTT Password (Default: no pw)")
parser.add_argument('-mqtthost', dest='mqtt_host', type=str, default="homeassistant.local",
                    help="MQTT Host (Default: homeassistant.local)")
parser.add_argument('-mqttport', dest='mqtt_port', type=int, default=1883,
                    help="MQTT Port (Default: 1883)")
parser.add_argument('-connect_on', dest='connect_on', type=any, default=GPIO.LOW,
                    help="Connect on (Default: GPIO.HIGH)")
parser.add_argument('-wsgp', dest='gpio_pump', type=int, default=11,
                    help="GPIO pin ump switch(Default: 11)")
parser.add_argument('-wsgb', dest='gpio_boiler', type=int, default=12,
                    help="GPIO pin boiler switch(Default: 12)")
parser.add_argument('-wsgfwev', dest='gpio_fresh_water_exit_valve', type=int, default=13,
                    help="GPIO pin freshwater exit Valve(Default: 13)")
parser.add_argument('-wsafwl', dest='ads_fresh_water_level_pin', type=int, default=0,
                    help="ADS pin freshwater level(Default: 0)")
parser.add_argument('-wsfwt', dest='fresh_water_temp_ds18b20_count', type=int, default=0,
                    help="freshwater temperature ds18b20 count(Default: 0)")
parser.add_argument('-wsgwwev', dest='gpio_waste_water_exit_valve', type=int, default=14,
                    help="GPIO pin wastewater exit Valve(Default: 14)")
parser.add_argument('-wsawwl', dest='ads_waste_water_level_pin', type=int, default=1,
                    help="ADS pin wastewater level(Default: 1)")
parser.add_argument('-wswwt', dest='waste_water_temp_ds18b20_count', type=int, default=1,
                    help="wastewater temperature ds18b20 count(Default: 2)")

args = parser.parse_args()

GPIO.setmode (GPIO.BCM)
GPIO.setwarnings(False)


client = mqtt.Client()
client.username_pw_set(args.mqtt_user, args.mqtt_password)

device_watersystem = Device(["Watersystem"], "watersystem", "v1", "rpi", "me")
watersystem = Watersystem("Watersystem", device_watersystem, client, args)
device_electric = Device(["Electric"], "electric", "v1", "rpi", "me")
device_gas = Device(["Gas"], "gas", "v1", "rpi", "me")
device_heating = Device(["Heating"], "heating", "v1", "rpi", "me")
connected = False
def on_message(client, userdata, message):
    watersystem.on_message(message)

def on_connect(client, userdata, flags, rc):
    watersystem.subscribe()
    connected = True

def on_disconnect(client, userdata, rc):
    connected = False

client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect(args.mqtt_host, args.mqtt_port)
client.loop_start()
systemd.daemon.notify('READY=1')
while True:
    watersystem.send_data()
    time.sleep(2)




