# -*- coding: utf-8 -*-
## based on https://github.com/karioja/vedirect.git
## written by https://github.com/karioja

import serial

class Vedirect:
    name_map = {
        'V': 'Voltage',
        'V2': 'Voltage CH2',
        'V3': 'Voltage CH3',
        'VS': 'Voltage Starter',
        'VM': 'Voltage Mid-Point',
        'DM': 'Deviation Mid-Point',
        'VPV': 'Voltage Panel',
        'PPV': 'Power Panel',
        'I': 'Current',
        'I2': 'Current CH2',
        'I3': 'Current CH3',
        'IL': 'Current Load',
        'LOAD': 'Load State',
        'T': 'Temperature',
        'P': 'Power',
        'CE': 'Consumed Amp Hours',
        'SOC': 'State-of-charge',
        'TTG': 'Time-to-go',
        'Alarm': 'Alarm',
        'Relay': 'Relay State',
        'AR': 'Alarm reason',
        'OR': 'Off reason',
        'H1': 'Depth of the deepest discharge',
        'H2': 'Depth of the last discharge',
        'H3': 'Depth of the average discharge',
        'H4': 'Number of charge cycles',
        'H5': 'Number of full discharges',
        'H6': 'Cumulative Amp Hours drawn',
        'H7': 'Minimum main (battery) voltage',
        'H8': 'Maximum main (battery) voltage',
        'H9': 'Number of seconds since last full charge',
        'H10': 'Number of automatic synchronizations',
        'H11': 'Number of low main voltage alarms',
        'H12': 'Number of high main voltage alarms',
        'H13': 'Number of low auxiliary voltage alarms',
        'H14': 'Number of high auxiliary voltage alarms',
        'H15': 'Minimum auxiliary (battery) voltage',
        'H16': 'Maximum auxiliary (battery) voltage',
        'H17': 'Amount of discharged energy/produced Energy',
        'H18': 'Amount of charged energy/consumed Energy',
        'H19': 'Yield total',
        'H20': 'Yiel today',
        'H21': 'Max Power today',
        'H22': 'Yield yesterday',
        'H23': 'Max Power yesterday',
        'Err': 'Error code',
        'CS': 'Operation State',
        'BMV': 'Model description',
        'FW': 'Firmware version',
        'FWE': 'Firmware version',
        'PID': 'Product ID',
        'SER#': 'Serial number',
        'HSDS': 'Day sequence number',
        'MODE': 'Device Mode',
        'AC_OUT_V': 'Voltage AC Output',
        'AC_OUT_I': 'Current AC Output',
        'AC_OUT_S': 'Power AC Output',
        'WARN': 'Warning reason',
        'MPPT': 'Tracker Operation mode',
        'MON': 'DC monitor mode',
        'DC_IN_V': 'Voltage DC Input',
        'DC_IN_I': 'Current DC Input',
        'DC_IN_P': 'Power DC Input'
    }

    measurement_map={
        'V': 'mV', 
        'V2': 'mV', 
        'V3': 'mV', 
        'VS': 'mV', 
        'VM': 'mV', 
        'DM': '‰', 
        'VPV': 'mV', 
        'PPV': 'W', 
        'I': 'mA', 
        'I2': 'mA', 
        'I3': 'mA', 
        'IL': 'mA', 
        'LOAD': 'on/off', 
        'T': 'C', 
        'P': 'W', 
        'CE': 'mAh', 
        'SOC': '‰', 
        'TTG': 'Minutes', 
        'Alarm': 'on/off', 
        'Relay': 'on/off', 
        'AR': 'Integer', 
        'OR': 'Integer', 
        'H1': 'mAh', 
        'H2': 'mAh', 
        'H3': 'mAh', 
        'H4': 'Integer', 
        'H5': 'Integer', 
        'H6': 'mAh', 
        'H7': 'mV', 
        'H8': 'mV', 
        'H9': 'Seconds', 
        'H10': 'Integer', 
        'H11': 'Integer',
        'H12': 'Integer', 
        'H13': 'Integer', 
        'H14': 'Integer', 
        'H15': 'mV', 
        'H16': 'mV', 
        'H17': '0.01 kWh', 
        'H18': '0.01 kWh', 
        'H19': '0.01 kWh', 
        'H20': '0.01 kWh', 
        'H21': 'W', 
        'H22': '0.01 kWh', 
        'H23': 'W', 
        'Err': 'Integer', 
        'CS': '', #TODO
        'BMV': 'String', 
        'FW': 'String', 
        'FWE': 'String', 
        'PID': 'String', 
        'SER#': 'String', 
        'HSDS': 'Integer', 
        'MODE': '', #TODO
        'AC_OUT_V': '0.01 V', 
        'AC_OUT_I': '0.1 A', 
        'AC_OUT_S': 'VA', 
        'WARN': 'Integer', 
        'MPPT': '', #TODO
        'MON': 'Integer', 
        'DC_IN_V': '0.01 V', 
        'DC_IN_I': 'A', 
        'DC_IN_P': 'W', 
    }

    def __init__(self, serialport, timeout):
        self.serialport = serialport
        self.ser = serial.Serial(serialport, 19200, timeout=timeout)
        self.header1 = ord('\r')
        self.header2 = ord('\n')
        self.hexmarker = ord(':')
        self.delimiter = ord('\t')
        self.key = ''
        self.value = ''
        self.bytes_sum = 0;
        self.state = self.WAIT_HEADER
        self.dict = {}


    (HEX, WAIT_HEADER, IN_KEY, IN_VALUE, IN_CHECKSUM) = range(5)

    def input(self, byte):
        if byte == self.hexmarker and self.state != self.IN_CHECKSUM:
            self.state = self.HEX
            
        
        if self.state == self.WAIT_HEADER:
            self.bytes_sum += byte
            if byte == self.header1:
                self.state = self.WAIT_HEADER
            elif byte == self.header2:
                self.state = self.IN_KEY

            return None
        elif self.state == self.IN_KEY:
            self.bytes_sum += byte
            if byte == self.delimiter:
                if (self.key == 'Checksum'):
                    self.state = self.IN_CHECKSUM
                else:
                    self.state = self.IN_VALUE
            else:
                self.key += chr(byte)
            return None
        elif self.state == self.IN_VALUE:
            self.bytes_sum += byte
            if byte == self.header1:
                self.state = self.WAIT_HEADER
                self.dict[self.key] = self.value;
                self.key = '';
                self.value = '';
            else:
                self.value += chr(byte)
            return None
        elif self.state == self.IN_CHECKSUM:
            self.bytes_sum += byte
            self.key = ''
            self.value = ''
            self.state = self.WAIT_HEADER
            if (self.bytes_sum % 256 == 0):
                self.bytes_sum = 0
                return self.dict
            else:
                self.bytes_sum = 0
        elif self.state == self.HEX:
            self.bytes_sum = 0
            if byte == self.header2:
                self.state = self.WAIT_HEADER
        else:
            raise AssertionError()

    def read_data_single(self):
        while True:
            data = self.ser.read()
            for single_byte in data:
                packet = self.input(single_byte)
                if (packet != None):
                    return packet