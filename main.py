import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

pin = 17

GPIO.setup(pin,GPIO.OUT)
led_pwm = GPIO.PWM(pin, 100)

led_pwm.start(0)

try:
    while True:
        for dc in range(0, 101, 5):
            led_pwm.ChangeDutyCycle(dc)
            time.sleep(1)
        for dc in range(100, -1, -5):
            led_pwm.ChangeDutyCycle(dc)
            time.sleep(1)
except KeyboardInterrupt:
    print("\n End")
finally:
    led_pwm.stop()
    GPIO.cleanup()

