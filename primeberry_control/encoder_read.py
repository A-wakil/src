from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import sys
import os
import serial

lock_file = '/tmp/myprogram.lock'

if os.path.exists(lock_file):
    sys.exit()

open(lock_file, 'w').close()

try:
    # Initialize the serial connection
    ser = serial.Serial('/dev/ttyACM0', 9600)

    # Create a default object for the motor HAT
    mh = Adafruit_MotorHAT()

    # Select the motor ID (M1, M2, M3, or M4)
    motor_id = 1
    motor2_id = 2

    # Get the motor objects based on the motor IDs
    motor = mh.getMotor(motor_id)
    motor2 = mh.getMotor(motor2_id)

    # Set the motor speed (0 to 255) and direction
    speed = 200
    direction = Adafruit_MotorHAT.FORWARD

    # Set the duration to run the motors (in seconds)
    run_duration = 8  # Change this to 8-10 seconds as needed

    # Function to control the motors
    def control_motors():
        motor.setSpeed(speed)
        motor2.setSpeed(speed)
        motor.run(direction)
        motor2.run(direction)

    # Start the motors
    control_motors()

    # Note the start time
    start_time = time.time()

    # Main loop to read encoder data and check the timer
    while True:
        # Check if the run duration has passed
        if time.time() - start_time >= run_duration:
            # Stop the motors
            motor.run(Adafruit_MotorHAT.RELEASE)
            motor2.run(Adafruit_MotorHAT.RELEASE)
            break

        # Read and print the encoder position
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8', errors='replace').strip()
            print(data)
            # try:
            #     positionl, positionr = map(int, data.split('s'))
            #     print(f"Positionl: {positionl}, Positionr: {positionr}")
            # except ValueError:
            #     print(f"Received invalid data: {data}")

finally:
    os.remove(lock_file)
    ser.close()  # Close the serial connection when done
