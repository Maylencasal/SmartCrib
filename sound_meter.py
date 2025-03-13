import sounddevice as sd
import numpy as np
import time

# ✅ Adjusted for I2S microphone
SAMPLE_RATE = 48000
DEVICE = "hw:1,0"
DURATION = 0.5  # ✅ Keep the same duration
BASELINE_DB = 75  # ✅ Makes 75 dB → 0 dB
AMPLIFICATION_FACTOR = 3.0  # ✅ Increase to enhance small variations

def get_decibel_level():
    """Capture audio and calculate adjusted decibel level."""
    try:
        audio_data = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE,
                            channels=1, dtype='int32', device=DEVICE)
        sd.wait()

        # ✅ Normalize 32-bit integer to float (-1 to 1)
        audio_data = audio_data.astype(np.float32) / np.iinfo(np.int32).max

        # ✅ Compute RMS (Root Mean Square) value
        rms_value = np.sqrt(np.mean(audio_data ** 2))

        # ✅ Convert to decibels
        decibels = 20 * np.log10(rms_value + 1e-6)

        # ✅ Adjust the dB scale so 75 dB → 0 dB and amplify variations
        adjusted_db = (decibels + 100 - BASELINE_DB) * AMPLIFICATION_FACTOR

        return round(adjusted_db, 2)

    except Exception as e:
        print(f"I2S Audio Error: {e}")
        return -1  # Return -1 if an error occurs

def continuously_update_sound_level():
    """Continuously update sound_level.txt with the latest decibel level."""
    while True:
        sound_level = get_decibel_level()
        with open("sound_level.txt", "w") as sound_file:
            sound_file.write(str(sound_level))  # ✅ Write to file
        time.sleep(1)  # ✅ Update every second

if __name__ == "__main__":
    print("🔊 Continuously updating sound_level.txt... (Press CTRL+C to stop)")
    continuously_update_sound_level()
