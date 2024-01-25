import json
import paho.mqtt.client as mqtt
from ..device import *
from ..shared.ve_direct_to_python import * 
class SmartShunt():
    def __init__(self, name, uniq_id, device: Device, client: mqtt.Client, serial_port, aux_input=None):
        self.name = name
        self.device = device
        self.client = client
        self.uniq_id = uniq_id
        self.topic = "homeassistant/sensor/" + self.device.name + "/" + self.uniq_id
        self.ve = Vedirect(serial_port, 19200)
        self.keys=['V','I','P','CE','SOC','TTG','Alarm','AR','H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12','H15','H16','H17','H18','BMV','FW','PID','MON']
        if aux_input == 'Starter':
            self.keys.append('VS')
        if aux_input == 'Mid Point':
            self.keys.append('VM')
            self.keys.append('DM')
        if aux_input == 'Temperature':
            self.keys.append('T')
        self.initiated_keys = []
          
        
    def send_config(self):
        for key in self.keys:
            name = Vedirect.name_map[key]
            mod_name = name.strip().replace(' ','_').lower()
            unit = Vedirect.measurement_map[key]
            conf = {
                "name": self.name + '_' + mod_name,
                "state_topic": self.topic + '_' + mod_name + "/state",
                "state_class": "measurement",
                "unit_of_measurement": unit,
                "value_template": "{{ value }}",
                "unique_id": self.uniq_id + '_' + mod_name,
                "device": self.device,
                "platform": "mqtt"
            }
            if unit == 'on/off':
                conf = {
                    "name": self.name + '_' + mod_name,
                    "state_topic": self.topic + '_' + mod_name + "/state",
                    "state_class": "binary",
                    "value_template": "{{ value }}",
                    "unique_id": self.uniq_id + '_' + mod_name,
                    "device": self.device,
                    "payload_off":"off",
                    "payload_on":"on",
                    "platform": "mqtt"
                }
            if unit == 'Integer' or unit == 'String':
                conf = {}
            if conf != {}:
                print(mod_name)
                self.client.publish(self.topic + '_' + mod_name + "/config",json.dumps(conf), 0, True)
                self.initiated_keys.append(key)
    
    def send_data(self):
        data = self._read_data()
        for key in self.initiated_keys:
            name = Vedirect.name_map[key]
            mod_name = name.strip().replace(' ','_').lower()
            print(mod_name)
            if(key in data.keys()):
                print(data[key])
                self.client.publish(self.topic + '_' + mod_name + "/state", str(data[key]), 0, False)

    def _read_data(self):
        return self.ve.read_data_single()