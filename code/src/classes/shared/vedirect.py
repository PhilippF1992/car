import json
import paho.mqtt.client as mqtt
from ..device import *
from .vedirect_serial import *
from .maps import *

class Vedirect:
    def __init__(self, name, uniq_id, device: Device, client: mqtt.Client, serial_port, keys):
        self.name = name
        self.device = device
        self.client = client
        self.uniq_id = uniq_id
        self.ve = VedirectSerial(serial_port, 19200)
        self.initiated_keys = []
        self.keys = keys
  
    def mod_name(self, name):
        return name.strip().replace(' ','_').replace('(','_').replace(')','_').replace('/','_').lower()
    
    def _send_config_total(self, key):
        name = Maps.name_map[key]
        mod_name = self.mod_name(name)
        topic = "homeassistant/sensor/" + self.device.name + "/" + self.uniq_id
        conf = {
            "name": self.name + '_' + mod_name,
            "state_topic": topic + '_' + mod_name + "/state",
            "state_class": "total",
            "value_template": "{{ value }}",
            "unique_id": self.uniq_id + '_' + mod_name,
            "device": self.device,
            "platform": "mqtt"
        }
        self.client.publish(topic + '_' + mod_name + "/config",json.dumps(conf), 0, True)
        self.initiated_keys.append(key)

    def _send_config_text(self, key):
        name = Maps.name_map[key]
        mod_name = self.mod_name(name)
        topic = "homeassistant/sensor/" + self.device.name + "/" + self.uniq_id
        conf = {
            "name": self.name + '_' + mod_name,
            "state_topic": topic + '_' + mod_name + "/state",
            "value_template": "{{ value }}",
            "unique_id": self.uniq_id + '_' + mod_name,
            "device": self.device,
            "platform": "mqtt"
        }
        self.client.publish(topic + '_' + mod_name + "/config",json.dumps(conf), 0, True)
        self.initiated_keys.append(key)

    def _send_config_binary(self, key):
        name = Maps.name_map[key]
        mod_name = self.mod_name(name)
        topic = "homeassistant/binary_sensor/" + self.device.name + "/" + self.uniq_id
        conf = {
            "name": self.name + '_' + mod_name,
            "state_topic": topic + '_' + mod_name + "/state",
            "state_class": "binary",
            "value_template": "{{ value }}",
            "unique_id": self.uniq_id + '_' + mod_name,
            "device": self.device,
            "payload_off":"OFF",
            "payload_on":"ON",
            "platform": "mqtt"
        }
        self.client.publish(topic + '_' + mod_name + "/config",json.dumps(conf), 0, True)
        self.initiated_keys.append(key)

    def _send_config_measurement(self, key):
        name = Maps.name_map[key]
        mod_name = self.mod_name(name)
        unit = Maps.measurement_map[key]
        if ' ' in unit:
            unit = unit.split(' ')[1]
        topic = "homeassistant/sensor/" + self.device.name + "/" + self.uniq_id
        conf = {
            "name": self.name + '_' + mod_name,
            "state_topic": topic + '_' + mod_name + "/state",
            "state_class": "measurement",
            "unit_of_measurement": unit,
            "value_template": "{{ value }}",
            "unique_id": self.uniq_id + '_' + mod_name,
            "device": self.device,
            "platform": "mqtt"
        }
        self.client.publish(topic + '_' + mod_name + "/config",json.dumps(conf), 0, True)
        self.initiated_keys.append(key)

    def send_config(self):
        for key in self.keys:
            unit = Maps.measurement_map[key]
            if unit == 'on/off': #Binary Sensors
                self._send_config_binary(key)
            elif unit == 'total':
                self._send_config_total(key) 
            elif unit == 'text':
                self._send_config_text(key)    
            elif unit == 'text_map':
                self._send_config_text(key)
            else: #Measurements (maybe with factor)
                self._send_config_measurement(key)

    def _send_data_binary(self, key, data):
        name = Maps.name_map[key]
        mod_name = self.mod_name(name)
        topic = "homeassistant/binary_sensor/" + self.device.name + "/" + self.uniq_id
        if(key in data.keys()):
            self.client.publish(topic + '_' + mod_name + "/state", str(data[key]), 0, False)

    def _send_data_total(self, key, data):
        name = Maps.name_map[key]
        mod_name = self.mod_name(name)
        topic = "homeassistant/sensor/" + self.device.name + "/" + self.uniq_id
        if(key in data.keys()):
            self.client.publish(topic + '_' + mod_name + "/state", str(data[key]), 0, False)

    def _send_data_text(self, key, data):
        name = Maps.name_map[key]
        mod_name = self.mod_name(name)
        topic = "homeassistant/sensor/" + self.device.name + "/" + self.uniq_id
        if(key in data.keys()):
            self.client.publish(topic + '_' + mod_name + "/state", str(data[key]), 0, False)

    def _send_data_text_map(self, key, data):
        name = Maps.name_map[key]
        mod_name = self.mod_name(name)
        topic = "homeassistant/sensor/" + self.device.name + "/" + self.uniq_id
        if(key in data.keys()):
            value = self.mod_name(Maps.text_maps[key][str(data[key])])
            self.client.publish(topic + '_' + mod_name + "/state", str(value), 0, False)

    def _send_data_measurement(self, key, data):
        name = Maps.name_map[key]
        mod_name = self.mod_name(name)
        unit = Maps.measurement_map[key]
        factor = 1
        if ' ' in unit:
            factor = float(unit.split(' ')[0])
        topic = "homeassistant/sensor/" + self.device.name + "/" + self.uniq_id
        if(key in data.keys()):
            value = float(data[key]) * factor
            self.client.publish(topic + '_' + mod_name + "/state", str(value), 0, False)
  
    def send_data(self):
        data = self._read_data()
        for key in self.initiated_keys:
            unit = Maps.measurement_map[key]
            if unit == 'on/off': #Binary Sensors
                self._send_data_binary(key, data)
            elif unit == 'total':
                self._send_data_total(key, data)
            elif unit == 'text':
                self._send_data_text(key, data)
            elif unit == 'text_map':
                self._send_data_text_map(key, data)
            else:
                self._send_data_measurement(key, data)

    def _read_data(self):
        return self.ve.read_data_single()