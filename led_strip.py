import board
import neopixel

# LED Strip Configuration
LED_PIN = board.D18  # GPIO 18 (Pin 12)
NUM_LEDS = 60  # Change this to the number of LEDs on your strip

# Initialize the LED strip
strip = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=1.0, auto_write=True)

# Turn all LEDs white
strip.fill((255, 255, 255))  # RGB (255,255,255) = White

