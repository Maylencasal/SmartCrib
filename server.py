import board
import neopixel
from flask import Flask, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/monitor")
def monitor_page():
    """Serve an HTML page that shows both temperature and sound levels, stacked with navigation."""
    return render_template("index.html")



@app.route("/api/sound")
def api_get_sound_level():
    """Return the latest sound level in JSON format & update LEDs."""
    try:
        with open("sound_level.txt") as sound_level:
            db_level = float(sound_level.read())  # Convert to float

        update_leds(db_level)  # Update LEDs based on sound

        return jsonify({"decibels": db_level})  # Send JSON response

    except Exception as e:
        return jsonify({"error": str(e)})  # Error handling

@app.route("/sound")
def get_sound_level():
    """Serve an HTML page that updates the sound level every second."""
    return render_template("sound.html")


@app.route("/temperature")
def get_temperature():
    try:
        temp_output = subprocess.check_output(["python3", "temperature.py"]).decode("utf-8").strip()
        temp_c = float(temp_output.replace("°C", "").strip())  # Extract numerical value
        temp_f = (temp_c * 9/5) + 32  # Convert to Fahrenheit

        # Determine warning message and blinking light color
        warning_message = ""
        warning_class = ""
        light_class = ""
        
        if temp_f > 75:
            warning_message = "⚠️ Too Hot! Be sure to adjust the temperature."
            warning_class = "warning-box"
            light_class = "blinking hot-light"
        elif temp_f < 65:
            warning_message = "❄️ Too Cold! Be sure to adjust the temperature."
            warning_class = "warning-box"
            light_class = "blinking cold-light"

        return render_template("temperature.html", warning=warning_message, temp_c=temp_c, temp_f=temp_f)
    except Exception as e:
        return f"<p>Error reading temperature: {str(e)}</p>"

@app.route("/api/temperature")
def api_get_temperature():
    """Return the latest temperature in JSON format."""
    try:
        temp_output = subprocess.check_output(["python3", "temperature.py"]).decode("utf-8").strip()
        temp_c = float(temp_output.replace("°C", "").strip())  # Extract numerical value
        temp_f = (temp_c * 9/5) + 32  # Convert to Fahrenheit
        return jsonify({"temp_c": temp_c, "temp_f": temp_f})
    except Exception as e:  # 🔹 Make sure this line exists
        return jsonify({"error": str(e)})  # 🔹 This was missing, 

# LED Setup
LED_PIN = board.D12  # GPIO12
NUM_LEDS = 60
BRIGHTNESS = 0.5
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

def update_leds(db_level):
    """Update LEDs based on sound level"""
    if db_level <= 2:
        color = (255, 255, 255)  # White
    elif 2 < db_level <= 16:
        color = (255, 255, 0)  # Yellow
    else:
        color = (255, 0, 0)  # Red (Flashing)
    
    pixels.fill(color)
    pixels.show()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

