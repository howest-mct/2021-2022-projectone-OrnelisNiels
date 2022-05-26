from RPi import GPIO
import time
from smbus import SMBus


class RGB:
    def __init__(self, rood, groen, blauw):
        self.rood = rood
        self.groen = groen
        self.blauw = blauw
        self.rgb = [self.rood, self.groen, self.blauw]

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rgb, GPIO.OUT)
        self.ledPWMRood = GPIO.PWM(self.rood, 1000)
        self.ledPWMGroen = GPIO.PWM(self.groen, 1000)
        self.ledPWMBlauw = GPIO.PWM(self.blauw, 1000)
        self.ledPWMRood.start(0)
        self.ledPWMGroen.start(0)
        self.ledPWMBlauw.start(0)

    def RGB_set(self, rood, groen, blauw):
        self.ledPWMRood.ChangeDutyCycle(rood)
        self.ledPWMGroen.ChangeDutyCycle(groen)
        self.ledPWMBlauw.ChangeDutyCycle(blauw)
