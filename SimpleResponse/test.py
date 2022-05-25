from rgbKlasse import RGB
from RPi import GPIO
import time
rood = 5
groen = 6
blauw = 22

try:
    rgb = RGB(rood, groen, blauw)
    rgb.RGB_set(0, 100, 100)
    while True:
        rgb.RGB_set(0, 0, 100)
        time.sleep(0.5)
        rgb.RGB_set(25, 50, 0)
        time.sleep(0.5)
        rgb.RGB_set(75, 60, 10)
        time.sleep(0.5)

finally:
    GPIO.cleanup()
