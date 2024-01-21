import json
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from ..device import *
from gpio_switch import *

class GPIO_DIMM:
    def __init__(self, name, uniq_id, device: Device, client: mqtt.Client, pin, pin_switch, connect_on):
        self.name = name
        self.device = device
        self.client = client
        self.uniq_id = uniq_id
        self.pin = pin
        self.topic = "homeassistant/switch/" + self.device.name + "/" + self.uniq_id
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50)
        self.pwm.start(0)
        self.switch = GPIO_Switch(name + " Switch", name +"_switch", device, client, pin_switch, connect_on, uniq_id)
        self._send_config()

    def _send_config(self):
        conf = {
            "name": self.name,
            "state_topic": self.topic + "/state",
            "command_topic": self.topic + "/set",
            "state_value_template": "{% if value|int > 0 %}1{% else %}0{% endif %}",
            "on_command_type": "brightness",
            "unique_id": self.uniq_id,
            "device": self.device,
            "payload_off":"False",
            "payload_on":"True",
            "state_off":"False",
            "state_on":"True",
            "brightness_state_topic": self.topic + "/state",
            "brightness_command_topic": self.topic + "/set",
            "brightness_scale": 100,
            "qos": 1,
            "platform": "mqtt"
        }
        self.client.publish(self.topic + "/config",json.dumps(conf), 0, True)
        self._send_data(0)

    def _send_data(self, data):
        self.client.publish(self.topic + "/state", str(data), 0, False)
    
    def set_off(self):
        self._send_data(0)
        self.pwm.ChangeDutyCycle(0)
        self.switch.set_off()

    def set_value(self, value):
        self._send_data(value)
        self.pwm.ChangeDutyCycle(value)
        self.switch.set_on()

    def on_message(self, message):
        if (message.topic == self.topic + "/set"):
            payload=float(message.payload.decode("utf-8"))
            if (payload > 0):
                self.set_value(payload)
            else: 
                self.set_off()
