import board
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, 0x20)

pin0 = mcp.get_pin(0)
pin0.direction = digitalio.Direction.INPUT

print(pin0.value)