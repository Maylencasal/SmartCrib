#!/bin/bash
PID=$(cat sound_pid.txt)
kill -9 $PID
python3 sound_meter.py 2> /dev/null &
echo $! > sound_pid.txt
