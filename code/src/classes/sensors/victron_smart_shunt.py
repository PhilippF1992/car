import paho.mqtt.client as mqtt
from ..device import *
from ..shared.vedirect import * 

class SmartShunt(Vedirect):
    def __init__(self, name, uniq_id, device: Device, client: mqtt.Client, serial_port):
        keys=['V','VS','VM','DM','T','I','P','CE','SOC','TTG','Alarm','AR','H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12','H15','H16','H17','H18','BMV','FW','PID','MON']
        super().__init__(name, uniq_id, device, client, serial_port, keys)
    
    