
from RPi import GPIO
import time
from smbus import SMBus


class lcdKlasse():
    def __init__(self, rs, e, databits=[], pcf=False) -> None:
        self.databits = databits
        self.rs = rs
        self.e = e
        self.teller = 0
        self.pcf = pcf
        if self.pcf == True:
            self.i2c = SMBus()
            self.i2c.open(1)

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.e, GPIO.OUT)
        # GPIO.setup(self.databits, GPIO.OUT, initial=GPIO.LOW)

    def send_instruction(self, value):
        GPIO.output(self.rs, GPIO.LOW)
        self.set_data_bits(value)
        GPIO.output(self.e, GPIO.HIGH)
        GPIO.output(self.e, GPIO.LOW)
        time.sleep(0.01)

    def send_character(self, value):
        GPIO.output(self.rs, GPIO.HIGH)
        self.set_data_bits(value)
        GPIO.output(self.e, GPIO.HIGH)
        GPIO.output(self.e, GPIO.LOW)
        time.sleep(0.01)

    def set_data_bits(self, value):
        if self.pcf == False:
            mask = 0b00000001
            for i in range(0, 8):
                if (value & mask) > 0:
                    GPIO.output(self.databits[i], GPIO.HIGH)
                else:
                    GPIO.output(self.databits[i], GPIO.LOW)
            mask = mask << 1
        else:
            self.i2c.write_byte(0x20, value)

    def send_message(self, woord):
        for letter in woord:
            self.teller += 1
            self.send_character(ord(letter))
            if (self.teller == 16):
                self.send_instruction(0b10000000 | 0x40)

    def init_LCD(self):
        self.send_instruction(0b00111000)
        self.send_instruction(0b00001111)
        self.send_instruction(0b00000001)

    def reset_lcd(self):
        print('test')
        self.send_instruction(0b00000001)

    def set_cursor(self, value):
        self.send_instruction(0b10000000 | value)

    def reset_cursor(self):
        self.send_instruction(0b00000010)

    def eerste_rij(self):
        self.teller = 0
        self.send_instruction(0b10000000)

    def tweede_rij(self):
        self.teller = 0
        self.send_instruction(0b10000000 | 0x40)
