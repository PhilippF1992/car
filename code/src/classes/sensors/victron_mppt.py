import paho.mqtt.client as mqtt
from ..device import *
from ..shared.vedirect import * 

class Mppt(Vedirect):
    def __init__(self, name, uniq_id, device: Device, client: mqtt.Client, serial_port):
        keys=['V','VPV', 'PPV', 'I', 'IL', 'LOAD','OR','H19','H20','H21','H22','H23','ERR','CS','FW','PID','SER#']
        super().__init__(name, uniq_id, device, client, serial_port, keys)
    
    