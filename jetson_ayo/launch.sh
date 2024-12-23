#!/bin/bash

# Path to my executables
PYTHON39=/usr/local/bin/python3.9
PYTHON36=/usr/bin/python3.6

INFTEST_SCRIPT=/home/jetson/inftest2.py
CTEST2_SCRIPT=/home/jetson/ctest3.py

echo "Running inftest.py with Python 3.9..."
$PYTHON39 $INFTEST_SCRIPT &

INFT_PID=$!

sleep 10

echo "Running ctest2.py with Python 3.6..."
$PYTHON36 $CTEST2_SCRIPT

kill $INFT_PID

echo "Both scripts have been executed."
