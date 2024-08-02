import time
import systemd.daemon
import paho.mqtt.client as mqtt
from classes.device import *
from classes.actors.gpio_switch import *
from classes.actors.gpio_dimm import *
from classes.sensors.ds18b20 import *
from classes.sensors.ads1115 import *
from classes.sensors.gpio_input import *
from classes.sensors.victron_smart_shunt import *
from classes.sensors.victron_mppt import *
from configparser import ConfigParser

#Read config.ini file
config_object = ConfigParser()
config_object.read("config/config.ini")

if config_object.sections()==[]:
    print("Configurations not found!")
    print("Please run 'python configure.py' and restart")
else:    
    pin_config_object=ConfigParser()
    pin_config_object.read('config/pin_config.ini')
    #GPIO setup
    GPIO.setmode (GPIO.BCM)
    GPIO.setwarnings(False)
    #Basic setup mqtt-client & device
    client = mqtt.Client()
    client.username_pw_set(config_object['mqtt']['user'], config_object["mqtt"]["password"])
    
    #Basic setup Device for HA
    device = Device([config_object['base']['name']], config_object['base']['name'].strip().replace(' ','_'), "v1", "rpi", "me")
    
    #Create configured objects
    #relays
    relays=[]
    if ('relays' in config_object.sections()):
        for (key, value) in config_object.items('relays'):
            name = value
            uniq_id = value.strip().replace(' ','_')
            pin = pin_config_object["relays"][key]
            connect_on = pin_config_object["relays"]["connect_on"]
            relay = GPIO_Switch(name, uniq_id, device, client, pin, connect_on)
            relays.append(relay)

    #dimmers
    dimmers=[]
    if ('dimmers' in config_object.sections()):
        for (key, value) in config_object('dimmers'):
            name = value
            uniq_id = value.strip().replace(' ','_')
            pin = pin_config_object["dimmers"][key]
            dimmer = GPIO_DIMM(name, uniq_id, device, client, pin)
            dimmers.append(dimmer)

    #ds18b20
    ds18b20s=[]
    if ('ds18b20s' in config_object.sections()):
        for (key, value) in config_object('ds18b20'):
            name = value
            uniq_id = value.strip().replace(' ','_')
            one_wire_count = 0
            ds18b20 = DS18B20(name, uniq_id, device, client, one_wire_count)
            ds18b20s.append(ds18b20)

    #gpio_input
    gpio_inputs=[]
    if ('gpio_input' in config_object.sections()):
        for (key, value) in config_object('gpio_input'):
            name = value
            uniq_id = value.strip().replace(' ','_')
            pin = pin_config_object["gpio_input"][key]
            gpio_input = GPIO_Input(name, uniq_id, device, client, pin)
            gpio_inputs.append(gpio_input)
    
    #victron_smart_shunt_device = Device('Victron Smart Shunt', 'victron_smart_shunt', 1, 'rpi', 'me')
    #victron_smart_shunt = SmartShunt('smart_shunt', 'smart_shunt', victron_smart_shunt_device, client, '/dev/ttyUSB0')
    #victron_mppt_device = Device('Victron Mppt 100/45', 'victron_mppt_100_45', 1, 'rpi', 'me')
    #victron_mppt = Mppt('mppt', 'mppt', victron_mppt_device, client, '/dev/ttyUSB1')
    #handle messages received via mqtt
    def on_message(client, userdata, message):
        for relay in relays:
            relay.on_message(message)
        for dimmer in dimmers:
            dimmer.on_message(message)

    #handle connection
    connected = False
    def on_connect(client, userdata, flags, rc):
        for relay in relays:
            relay.send_config()
            relay.subscribe()
        for dimmer in dimmers:
            dimmer.subscribe()
            dimmer.send_config
        for ds18b20 in ds18b20s:
            ds18b20.send_config()
        for gpio_input in gpio_inputs:
            gpio_input.send_config()
        victron_smart_shunt.send_config()
        victron_mppt.send_config()
        connected = True

    def on_disconnect(client, userdata, rc):
        connected = False

    client.on_message = on_message
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect(config_object['mqtt']["host"], int(config_object['mqtt']["port"]))
    client.loop_start()
    systemd.daemon.notify('READY=1')
    while True:
        for ds18b20 in ds18b20s:
            ds18b20.send_data()
        for gpio_input in gpio_inputs:
            gpio_input.send_data()
        #victron_smart_shunt.send_data()
        #victron_mppt.send_data()
        time.sleep(2)




