import json
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from ..device import *

class GPIO_DIMM:
    def __init__(self, name, uniq_id, device: Device, client: mqtt.Client, pin, parent= ""):
        self.name = name
        self.device = device
        self.client = client
        self.uniq_id = uniq_id
        self.pin = pin