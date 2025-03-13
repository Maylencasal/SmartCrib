#!/bin/bash

# Start sound meter in background
echo "Starting Sound Meter..."
nohup python3 /home/baby/SmartCrib/sound_meter.py > sound_meter.log 2>&1 &

# Wait a moment to ensure sound_meter starts properly
sleep 2

# Start LED control in background
echo "Starting LED Control..."
nohup /home/baby/SmartCrib/run_leds.sh > leds.log 2>&1 &

# Wait a moment to ensure LEDs start properly
sleep 2

# Start Flask server with sudo (to access GPIO)
echo "Starting Flask Server..."
sudo /home/baby/SmartCrib/VENV/bin/python3 /home/baby/SmartCrib/server.py > server.log 2>&1 &
