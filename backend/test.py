from RPi import GPIO
import time
GPIO.setmode(GPIO.BCM)
motor = 25
GPIO.setup(motor, GPIO.OUT)
ledpwm = GPIO.PWM(motor, 100000)
ledpwm.start(0)
try:
    while True:
        ledpwm.ChangeDutyCycle(100)

except KeyboardInterrupt:
    print("KB interrupt")
finally:
    ledpwm.stop()
    GPIO.cleanup()
