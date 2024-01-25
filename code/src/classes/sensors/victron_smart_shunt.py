import json
import paho.mqtt.client as mqtt
from ..device import *
from ..shared.ve_direct_to_python import * 
class SmartShunt():
    def __init__(self, name, uniq_id, device: Device, client: mqtt.Client, serial_port):
        self.name = name
        self.device = device
        self.client = client
        self.uniq_id = uniq_id
        self.ve = Vedirect(serial_port, 19200)
        self.keys=['V','VS','VM','DM','T','I','P','CE','SOC','TTG','Alarm','AR','H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12','H15','H16','H17','H18','BMV','FW','PID','MON']
        self.initiated_keys = []
    
    def mod_name(self, name):
        return name.strip().replace(' ','_').replace('(','_').replace(')','_').replace('/','_').lower()
    
    def _send_config_binary(self, key):
        name = Vedirect.name_map[key]
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
        name = Vedirect.name_map[key]
        mod_name = self.mod_name(name)
        unit = Vedirect.measurement_map[key]
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
            unit = Vedirect.measurement_map[key]
            
            if unit == 'on/off': #Binary Sensors
                self._send_config_binary(key)
            elif unit == 'Integer' or unit == 'String': #Todo
                conf = {}
            else: #Measurements (maybe with factor)
                self._send_config_measurement(key)

    def _send_data_binary(self, key, data):
        name = Vedirect.name_map[key]
        mod_name = self.mod_name(name)
        unit = Vedirect.measurement_map[key]
        topic = "homeassistant/binary_sensor/" + self.device.name + "/" + self.uniq_id
        if(key in data.keys()):
            print(data[key])
            self.client.publish(topic + '_' + mod_name + "/state", str(data[key]), 0, False)

    def _send_data_measurement(self, key, data):
        name = Vedirect.name_map[key]
        mod_name = self.mod_name(name)
        unit = Vedirect.measurement_map[key]
        factor = 1
        if ' ' in unit:
            factor = float(unit.split(' ')[0])
        topic = "homeassistant/sensor/" + self.device.name + "/" + self.uniq_id
        if(key in data.keys()):
            value = float(data[key]) * factor
            print(mod_name)
            print(value)
            self.client.publish(topic + '_' + mod_name + "/state", str(value), 0, False)
    
    def send_data(self):
        data = self._read_data()
        for key in self.initiated_keys:
            unit = Vedirect.measurement_map[key]
            if unit == 'on/off': #Binary Sensors
                self._send_data_binary(key, data)
            elif unit == 'Integer' or unit == 'String': #Todo
                conf = {}
            else:
                self._send_data_measurement(key, data)

    def _read_data(self):
        return self.ve.read_data_single()