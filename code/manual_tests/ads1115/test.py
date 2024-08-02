import ADS1x15
import time
ADS = ADS1x15.ADS1115(1, 0x48)

ADS.setMode(ADS.MODE_SINGLE)    # SINGLE SHOT MODE
ADS.setGain(1)

#ADS.requestADC(0)
value = ADS.readADC(0)
value = ADS.readADC(0) #read twice to get correct data
print('1: ' + str(ADS.toVoltage(value)))
#time.sleep(0.5)
#ADS.requestADC(1)
value = ADS.readADC(1)
value = ADS.readADC(1)
print('2: ' + str(ADS.toVoltage(value)))
#time.sleep(0.5)
#ADS.requestADC(2)
value = ADS.readADC(2)
value = ADS.readADC(2)
print('3: ' + str(ADS.toVoltage(value)))
#time.sleep(0.5)
#ADS.requestADC(3)
value = ADS.readADC(3)
value = ADS.readADC(3)
print('4: ' + str(ADS.toVoltage(value)))