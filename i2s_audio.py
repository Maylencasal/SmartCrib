import sounddevice as sd
import numpy as np

# ✅ Sample rate must match your I2S mic
SAMPLE_RATE = 48000  
DEVICE = "hw:1,0"
DURATION = 0.5  # ✅ Keeping the same duration

# ✅ Define your baseline noise level (ambient noise level from your mic)
BASELINE_DB = 75  # This makes 75 dB become 0 dB

# ✅ Amplification factor to enhance small variations
AMPLIFICATION_FACTOR = 3.0  # Increase for more variance, reduce if too jumpy

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

print("Listening for sound levels... (Press CTRL+C to stop)")
while True:
    print(f"Adjusted dB Level: {get_decibel_level()} dB")
