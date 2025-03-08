import sounddevice as sd
import numpy as np
import threading
import time

SAMPLE_RATE = 16000  # Lower sample rate for stability
DURATION = 0.5  # Sample duration in seconds
latest_db = 0  # Store latest sound level globally

def capture_audio():
    """Continuously captures audio and updates latest_db value."""
    global latest_db
    while True:
        try:
            # Ensure device is available before recording
            if len(sd.query_devices()) == 0:
                print("No audio devices found!")
                latest_db = -1
                time.sleep(1)
                continue

            # 🔹 Open audio stream instead of restarting every second
            with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32') as stream:
                audio_data, _ = stream.read(int(SAMPLE_RATE * DURATION))

            # Calculate RMS (Root Mean Square) volume level
            rms_value = np.sqrt(np.mean(audio_data**2))

            # Convert to decibels (dB)
            decibels = 20 * np.log10(rms_value + 1e-6)  # Avoid log(0)

            # Normalize so silence is 0 dB
            latest_db = round(decibels + 30, 2)

        except sd.PortAudioError as e:
            print(f"Background Audio Error: {e}")
            latest_db = -1  # Error indicator

        except Exception as e:
            print(f"Unexpected Error: {e}")
            latest_db = -1  # Return -1 if an error occurs
        
        time.sleep(1)  # Wait 1 second before capturing again

# Start background audio processing
threading.Thread(target=capture_audio, daemon=True).start()

