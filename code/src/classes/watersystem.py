import time
from .device import *
from .switches.gpio_switch import *
from .sensors.ds18b20 import *
from .sensors.ads1115 import *
import paho.mqtt.client as mqtt

class Watersystem:
    def __init__(self, uniq_id, device: Device, client: mqtt.Client, gpio_pump, gpio_boiler, ads_fresh_water_level_pin, fresh_water_temp_ds18b20_count, ads_waste_water_level_pin, waste_water_temp_ds18b20_count, connect_on):
        self.uniq_id = uniq_id
        self.pump = GPIO_Switch("Pump", "pump", device, client, gpio_pump, connect_on, uniq_id)
        self.boiler = GPIO_Switch("Boiler", "boiler", device, client, gpio_boiler, connect_on, uniq_id)
        self.fresh_water_level = ADS1115("Freshwater Level", "fresh_water_level", device, client, ads_fresh_water_level_pin)
        self.fresh_water_temp = DS18B20("Freshwater Temperature", "freshwater_temperature", device, client, fresh_water_temp_ds18b20_count)
        self.waste_water_level = ADS1115("Freshwater Level", "fresh_water_level", device, client, ads_waste_water_level_pin)
        self.waste_water_temp = DS18B20("Wastewater Temperature", "wastewater_temperature", device, client, waste_water_temp_ds18b20_count)


    def subscribe(self):
        self.pump.subscribe()
        self.boiler.subscribe()

    def on_message(self, message):
        payload=str(message.payload.decode("utf-8"))
        if (self.pump.uniq_id in message.topic):
            if (payload=="True"):
                self.pump.set_on()
            else:
                self.pump.set_off()
                self.boiler.set_off()
        if (self.boiler.uniq_id in message.topic):
            if (payload=="True"):
                self.boiler.set_on()
            else:
                self.boiler.set_off()