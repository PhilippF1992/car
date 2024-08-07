import json
import paho.mqtt.client as mqtt
from ..device import *
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class ADS1115():
    def __init__(self, name, device: Device, client: mqtt.Client, address, factors):
        self.name = name
        self.device = device
        self.client = client
        self.address = address
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c, address=self.address)
        self.ads.gain = 1
        self.factors = factors
        self.base_topic = "homeassistant/sensor/" + self.device.name + "/" + self.name + "_"
        self.send_config()

    def send_config(self):
        for i in range(0,4):
            conf = {
                "name": self.name + f"_{i}",
                "state_topic": self.base_topic + f"{i}/state",
                "state_class": "measurement",
                "unit_of_measurement": "V",
                "value_template": "{{ value }}",
                "unique_id": self.name + f"_{i}",
                "device": self.device,
                "platform": "mqtt"
            }
            self.client.publish(self.base_topic + f"{i}/config",json.dumps(conf), 0, True)

    def send_data(self):
        for i in range(0,4):
            self.client.publish(self.base_topic + f"{i}/state", str(self._read_data(i)), 0, False)

    def _read_data(self, input):
        chan = AnalogIn(self.ads, input)
        return chan.voltage * self.factors[input]
    