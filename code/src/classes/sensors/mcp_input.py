import json
import paho.mqtt.client as mqtt
from ..device import *
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017

class MCP_Input():
    def __init__(self, name, device: Device, client: mqtt.Client, address):
        self.name = name
        self.device = device
        self.client = client
        self.address = address
        self.base_topic = "homeassistant/binary_sensor/" + self.device.name + "/" + self.name + "_"
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.mcp = MCP23017(self.i2c, self.address)
        for pin in range(0,16):
            mcp_pin = self.mcp.get_pin(pin)
            mcp_pin.direction = digitalio.Direction.INPUT
            mcp_pin.pull = digitalio.Pull.UP
            mcp_pin.invert_polarity = True
        self.send_config()

    def send_config(self):
        for pin in range(0,16):
            if pin < 10:
                name = self.name + f"_0{pin}"
            else:
                name =self.name + f"_{pin}"
            conf = {
                "name": name,
                "state_topic": self.base_topic + f"{pin}/state",
                "state_class": "binary",
                "value_template": "{{ value }}",
                "unique_id": name,
                "device": self.device,
                "payload_off":"False",
                "payload_on":"True",
                "platform": "mqtt"
            }
            self.client.publish(self.base_topic + f"{pin}/config",json.dumps(conf), 0, True)
        self.send_data()
    
    def send_data(self):
        for pin in range(0,16):
            self.client.publish(self.base_topic + f"{pin}/state", str(self._read_data(pin)), 0, False)

    def _read_data(self, pin):
        mcp_pin = self.mcp.get_pin(pin)
        return mcp_pin.value