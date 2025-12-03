import sys
import os

# --- Project path setup ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.transcription.whisper_transcriber import WhisperTranscriber

audio_path = "test.wav"

transcriber = WhisperTranscriber()
text = transcriber.transcribe(audio_path)

print("\n--- TRANSCRIPT ---\n")
print(text)
