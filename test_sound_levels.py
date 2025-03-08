import sounddevice as sd
import numpy as np

SAMPLE_RATE = 44100  # Sample rate (Hz)
DURATION = 0.5       # Sample duration in seconds

def get_decibel_level():
    """Capture audio and calculate the adjusted decibel level."""
    audio_data = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()

    # Calculate RMS (Root Mean Square) volume level
    rms_value = np.sqrt(np.mean(audio_data**2))
    
    # Convert to decibels (dB)
    decibels = 20 * np.log10(rms_value + 1e-6)  # Avoid log(0)

    # Normalize so silence is 0 dB
    adjusted_db = decibels + 30  # Shift scale (Change 30 to fine-tune if needed)
    
    return round(adjusted_db, 2)

print("Listening for sound levels... (Press CTRL+C to stop)")
while True:
    print(f"Adjusted dB Level: {get_decibel_level()} dB")

