import json
import glob
import paho.mqtt.client as mqtt
from ..device import *

class DS18B20():
    def __init__(self, name, device: Device, client: mqtt.Client, folder):
        self.name = name
        self.device = device
        self.client = client
        self.folder = folder
        self.file = folder + '/w1_slave'
        self.base_topic = "homeassistant/sensor/" + self.device.name + "/" + self.name
        self.send_config()

    def send_config(self):
        conf = {
            "name": self.name,
            "state_topic": self.base_topic + "/state",
            "state_class": "measurement",
            "unit_of_measurement": "C",
            "device_class": "temperature",
            "value_template": "{{ value }}",
            "unique_id": self.name,
            "device": self.device,
            "icon": "mdi:thermometer",
            "platform": "mqtt"
        }
        self.client.publish(self.base_topic + "/config",json.dumps(conf), 0, True)
    
    def send_data(self):
        self.client.publish(self.base_topic +  "/state", str(self._read_data()), 0, False)

    def _read_temp_raw(self):
        f = open(self.file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _read_data(self):
        lines = self._read_temp_raw()
        if lines[0].strip()[-3:] != 'YES':
            return 0
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c