import time
import neopixel
import board

# GPIO Pin for LEDs (Make sure it matches your setup)
LED_PIN = board.D12  # GPIO12
NUM_LEDS = 60
BRIGHTNESS = 0.5

# Initialize NeoPixel Strip
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

def get_sound_level():
    """Read the latest sound level from sound_level.txt."""
    try:
        with open("sound_level.txt", "r") as f:
            return float(f.read().strip())  # Convert to float
    except:
        return 0  # Default to 0 dB if there's an error

def update_leds():
    """Update LED color based on sound level."""
    while True:
        sound_level = get_sound_level()

        if sound_level < 2:
            pixels.fill((255, 255, 255))  # White
        elif 2 <= sound_level < 16:
            pixels.fill((255, 215, 0))  # Yellow
        else:
            pixels.fill((255, 0, 0))  # Red
        
        pixels.show()
        time.sleep(1)  # Update every second

if __name__ == "__main__":
    print("LED Strip is running based on sound levels...")
    update_leds()
