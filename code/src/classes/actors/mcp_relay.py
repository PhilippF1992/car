import json
import paho.mqtt.client as mqtt
from ..device import *
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017

class MCP_Relay:
    def __init__(self, name, device: Device, client: mqtt.Client, address, connect_on):
        self.name = name
        self.device = device
        self.client = client
        self.connect_on = True
        self.disconnect_on = False
        if (connect_on == 'False'):
            self.connect_on = False
            self.disconnect_on = True
        self.address = address
        self.base_topic = "homeassistant/switch/" + self.device.name + "/" + self.name + "_"

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.mcp = MCP23017(self.i2c, self.address)
        for pin in range(0,16):
            mcp_pin = self.mcp.get_pin(pin)
            mcp_pin.direction = digitalio.Direction.OUTPUT
            mcp_pin.value = self.disconnect_on

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
                "command_topic": self.base_topic + f"{pin}/set",
                "state_class": "binary",
                "value_template": "{{ value }}",
                "unique_id": name,
                "device": self.device,
                "payload_off":"False",
                "payload_on":"True",
                "state_off":"False",
                "state_on":"True",
                "platform": "mqtt"
            }
            self.client.publish(self.base_topic + f"{pin}/config",json.dumps(conf), 0, True)
            self._send_data(pin, False)

    def _send_data(self, pin, data):
        self.client.publish(self.base_topic + f"{pin}/state", str(data), 0, False)

    def set_off(self, pin):
        self._send_data(pin, False)
        self.mcp.get_pin(pin).value = self.disconnect_on

    def set_on(self, pin):
        self._send_data(pin, True)
        self.mcp.get_pin(pin).value = self.connect_on

    def subscribe(self):
        for pin in range(0,16):
            self.client.subscribe(self.base_topic + f"{pin}/set")

    def on_message(self, message):
        for pin in range(0,16):
            if (message.topic == self.base_topic + f"{pin}/set"):
                payload=str(message.payload.decode("utf-8"))
                if (payload == "True"):
                    self.set_on(pin)
                else: 
                    self.set_off(pin)

