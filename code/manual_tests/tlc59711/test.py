import board
import time
import busio
import adafruit_tlc59711
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
tlc59711 = adafruit_tlc59711.TLC59711(spi)


step = 1000
start_pwm = 0
end_pwm = 65535  # 100%:
tlc59711.r0 = 0
tlc59711.r1 = 0
tlc59711.r2 = 0
tlc59711.r3 = 0
tlc59711.g0 = 0
tlc59711.g1 = 0
tlc59711.g2 = 0
tlc59711.g3 = 0
tlc59711.b0 = 0
tlc59711.b1 = 0
tlc59711.b2 = 0
tlc59711.b3 = 0
while True:
    # Brighten:
    print("Brightening LED")
    for pwm in range(start_pwm, end_pwm, step):
        tlc59711.r0 = pwm
        print(pwm)
        time.sleep(1)

    # Dim:
    print("Dimming LED")
    for pwm in range(end_pwm, start_pwm, 0 - step):
        tlc59711.r0 = pwm
        print(pwm)
        time.sleep(1)