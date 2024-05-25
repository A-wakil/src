import RPi.GPIO as GPIO
import time

# GPIO pin for servo control
servo_pin = 6

# Setup GPIO using BOARD numbering
# GPIO.setmode(GPIO.BOARD)
# Setup GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)


# Setup servo pin as output
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM instance with frequency 50Hz
pwm = GPIO.PWM(servo_pin, 50)

# Start PWM with duty cycle for 0 degrees
# pwm.start(4.5)
# time.sleep(2)
pwm.start(9.5)
time.sleep(2)
pwm.ChangeDutyCycle(7)
time.sleep(2)
pwm.ChangeDutyCycle(4.5)
time.sleep(2)
pwm.ChangeDutyCycle(7)
time.sleep(2)



# for i in range(5):

#     pwm.ChangeDutyCycle(4.5)
#     time.sleep(5)

pwm.stop()
GPIO.cleanup()
