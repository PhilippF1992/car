from mcp23017 import *
from i2c import I2C
import smbus

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
i2c = I2C(smbus.SMBus(1))  # creates a I2C Object as a wrapper for the SMBus
mcp = MCP23017(0x21, i2c)   # creates an MCP object with the given address

mcp.pin_mode(GPB0, INPUT)
print(mcp.digital_read(GPB0))