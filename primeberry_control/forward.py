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
  

    # Get the motor object based on the motor ID
    motor = mh.getMotor(motor_id)
    motor2 = mh.getMotor(motor2_id)
  

    # Set the motor speed (0 to 255) and direction
    speed = 200
    direction = Adafruit_MotorHAT.FORWARD


    # Wait for a few seconds
    wait_time = 2


    motor.setSpeed(speed)
    motor2.setSpeed(speed)
    motor.run(direction)
    motor2.run(direction)
   
    time.sleep(wait_time)

    # Stop the motor
    motor.run(Adafruit_MotorHAT.RELEASE)
    motor2.run(Adafruit_MotorHAT.RELEASE)


finally:
    os.remove(lock_file)
