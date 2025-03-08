import sounddevice as sd
import numpy as np
import time

SAMPLE_RATE = 16000  # Lower sample rate for stability
DURATION = 0.5  # Sample duration in seconds

def start_collecting():
    finished_read = True
    while finished_read:
        value_read = _get_new_read()
        save_data(value_read)

def _process_stream_data(indata, frames, time, status):
    volume = np.linalg.norm(indata) * 10
    save_data(volume)

def save_data(reading):
    with open('sound_level.txt', 'w') as sound_file:
        sound_file.write(str(reading))
        sound_file.close()


def _get_new_read():
    """Capture audio and return decibel level."""
    try:
        audio_data = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait()

        # Calculate RMS volume
        rms_value = np.sqrt(np.mean(audio_data**2))

        # Convert to dB
        decibels = 20 * np.log10(rms_value + 1e-6)  # Avoid log(0)
        return round(decibels + 30, 2)  # Normalize to 0 dB baseline
    except Exception as e:
        #print(f"Sound Error: {e}")
        return -1  # Return -1 if error


if __name__ == "__main__":
    start_collecting()
#    with sd.InputStream(callback=_process_stream_data):
#        sd.sleep(500)

