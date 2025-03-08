import os
import glob
import time

# Find the sensor directory
base_dir = "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + "28*")[0]  # Detects the first DS18B20 sensor
device_file = device_folder + "/w1_slave"

def read_temp():
    """Reads temperature from the DS18B20 sensor using Linux's 1-Wire system."""
    with open(device_file, "r") as f:
        lines = f.readlines()
    
    # Retry if data is not yet ready
    while "YES" not in lines[0]:
        time.sleep(0.2)
        with open(device_file, "r") as f:
            lines = f.readlines()

    # Extract temperature value
    temp_string = lines[1].split("t=")[-1]
    temp_c = float(temp_string) / 1000.0
    return temp_c

if __name__ == "__main__":
    print(f"{read_temp():.3f}°C")
