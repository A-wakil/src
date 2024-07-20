#!/bin/bash

# Path to your Python executables
PYTHON39=/usr/local/bin/python3.9
PYTHON36=/usr/bin/python3.6

# Path to your Python scripts
INFTEST_SCRIPT=/home/jetson/inftest2.py
CTEST2_SCRIPT=/home/jetson/ctest3.py

# Run the inference server script with Python 3.9 in the background
echo "Running inftest.py with Python 3.9..."
$PYTHON39 $INFTEST_SCRIPT &

# Store the PID of the inference server
INFT_PID=$!

# Wait for the server to start up (you may adjust the sleep time as needed)
sleep 10

# Run the capture script with Python 3.6
echo "Running ctest2.py with Python 3.6..."
$PYTHON36 $CTEST2_SCRIPT

# Optionally, kill the inference server if you want to stop it after `ctest2.py` completes
kill $INFT_PID

echo "Both scripts have been executed."
