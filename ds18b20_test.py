import time
import board
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

# Change 'board.D5' to the correct pin your sensor is connected to.
ow_bus = OneWireBus(board.D4)

# Scan for sensors
devices = ow_bus.scan()
if not devices:
    print("No DS18B20 sensors found! Check wiring.")
else:
    print(f"Found {len(devices)} DS18B20 sensors.")

    # Get first sensor
    ds18b20 = DS18X20(ow_bus, devices[0])

    while True:
        print("Temperature: {:.3f}°C".format(ds18b20.temperature))
        time.sleep(1)
