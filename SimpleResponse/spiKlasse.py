import spidev
from RPi import GPIO
defaultspeed = 10 ** 5


class SpiClass:
    def __init__(self, bus, slave, speed=defaultspeed) -> None:
        self.bus = bus
        self.slave = slave
        self.speed = speed
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = speed

    def readChannel(self, channel):
        bytes_in = self.spi.xfer([1, (8 | channel) << 4, 0])
        resultaat = ((bytes_in[1] & 3) << 8) | bytes_in[2]
        return resultaat

    def close(self):
        self.spi.close()
