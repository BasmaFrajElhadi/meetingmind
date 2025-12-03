import sounddevice as sd
import numpy as np
import wave

def record_audio_stream():
    """
    Start recording audio from the microphone as a live stream.

    Args:
        samplerate (int, optional): Sampling rate in Hz. Default is 16000.
        channels (int, optional): Number of audio channels. Default is 1 (mono).

    Returns:
        tuple: (stream, recording_list, samplerate)
            - stream: The InputStream object (must be stopped externally).
            - recording_list: List to store captured audio chunks (numpy arrays).
            - samplerate: Sampling rate used.
    """
    fs = 16000
    recording = []

    def callback(indata, frames, time, status):
        recording.append(indata.copy())

    stream = sd.InputStream(samplerate=fs, channels=1, callback=callback)
    stream.start()
    return stream, recording, fs


def save_recording(recording, fs, filename):
    """
    Save a recorded audio stream to a WAV file.

    Args:
        recording (list): List of numpy arrays representing audio chunks.
        samplerate (int): Sampling rate used for recording.
        filename (str): Path to save the WAV file.

    Returns:
        str: Path to the saved WAV file.
    """
    audio = np.concatenate(recording, axis=0)

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes((audio * 32767).astype(np.int16).tobytes())


