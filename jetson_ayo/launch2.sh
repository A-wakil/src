#!/bin/bash

PYTHON39=/usr/local/bin/python3.9
PYTHON36=/usr/bin/python3.6


INFTEST_SCRIPT=/home/jetson/offline.py
CTEST2_SCRIPT=/home/jetson/coff.py

echo "Running offline.py with Python 3.9..."
$PYTHON39 $INFTEST_SCRIPT &

INFT_PID=$!

sleep 5

echo "Running coff.py with Python 3.6..."
$PYTHON36 $CTEST2_SCRIPT

kill $INFT_PID

echo "Both scripts have been executed."
