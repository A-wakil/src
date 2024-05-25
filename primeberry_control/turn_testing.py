import RPi.GPIO as GPIO
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import sys
import os

lock_file = '/tmp/myprogram.lock'

if os.path.exists(lock_file):
    sys.exit()

open(lock_file, 'w').close()

try:
    # Create a default object for the motor HAT
    mh = Adafruit_MotorHAT()

    # Select the motor ID (M1, M2, M3, or M4)
    motor_id = 1
    motor2_id = 2
    # GPIO pin for servo control
    servo_pin = 6

    # Get the motor object based on the motor ID
    motor = mh.getMotor(motor_id)
    motor2 = mh.getMotor(motor2_id)
    # Setup GPIO using BOARD numbering
    # GPIO.setmode(GPIO.BOARD)
    # Setup GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Setup servo pin as output
    GPIO.setup(servo_pin, GPIO.OUT)

    # Set the motor speed (0 to 255) and direction
    speed = 200
    direction = Adafruit_MotorHAT.FORWARD
    # Create PWM instance with frequency 50Hz
    pwm = GPIO.PWM(servo_pin, 50)

    # Wait for a few seconds
    wait_time = 2


    motor.setSpeed(speed)
    motor2.setSpeed(speed)
    motor.run(direction)
    motor2.run(direction)
    pwm.start(7)
    time.sleep(wait_time)
    time.sleep(wait_time)
    pwm.start(4.5)
    time.sleep(wait_time)
    pwm.start(7)
    time.sleep(wait_time)
    time.sleep(wait_time)


    # Stop the motor
    motor.run(Adafruit_MotorHAT.RELEASE)
    motor2.run(Adafruit_MotorHAT.RELEASE)

    pwm.stop()
    GPIO.cleanup()

finally:
    os.remove(lock_file)
