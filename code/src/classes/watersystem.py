import time
from .device import *
from .switches.gpio_switch import *
from .sensors.ds18b20 import *
from .sensors.ads1115 import *
import paho.mqtt.client as mqtt

class Watersystem:
    def __init__(self, uniq_id, device: Device, client: mqtt.Client, args):
        self.uniq_id = uniq_id
        self.pump = GPIO_Switch("Pump", "pump", device, client, args.gpio_pump, args.connect_on, uniq_id)
        self.boiler = GPIO_Switch("Boiler", "boiler", device, client, args.gpio_boiler, args.connect_on, uniq_id)
        self.fresh_water_exit_valve = GPIO_Switch("Freshwater Exit Valve", "fresh_water_exit_valve", device, client, args.gpio_fresh_water_exit_valve, args.connect_on, uniq_id)
        self.fresh_water_level = ADS1115("Freshwater Level", "fresh_water_level", device, client, args.ads_fresh_water_level_pin)
        self.fresh_water_temp = DS18B20("Freshwater Temperature", "freshwater_temperature", device, client, args.fresh_water_temp_ds18b20_count)
        self.waste_water_exit_valve = GPIO_Switch("Wastehwater Exit Valve", "waste_water_exit_valve", device, client, args.gpio_waste_water_exit_valve, args.connect_on, uniq_id)
        self.waste_water_level = ADS1115("Wastewater Level", "waste_water_level", device, client, args.ads_waste_water_level_pin)
        self.waste_water_temp = DS18B20("Wastewater Temperature", "wastewater_temperature", device, client, args.waste_water_temp_ds18b20_count)

    def send_data(self):
        self.fresh_water_level.send_data()
        self.fresh_water_temp.send_data()
        self.waste_water_level.send_data()
        self.waste_water_temp.send_data()

    def subscribe(self):
        self.pump.subscribe()
        self.boiler.subscribe()

    def on_message(self, message):
        self.pump.on_message(message)
        self.boiler.on_message(message)