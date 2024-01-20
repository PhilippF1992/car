import json
import glob
import time
import paho.mqtt.client as mqtt
from ..device import *

class ADS1115():
    def __init__(self, name, uniq_id, device: Device, client: mqtt.Client, ads_pin):
        self.name = name
        self.device = device
        self.client = client
        self.uniq_id = uniq_id