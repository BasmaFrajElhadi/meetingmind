from pathlib import Path
import librosa
import soundfile as sf
import noisereduce as nr
import logging
import sys
import os

from src.handlers.error_handler import handle_errors, MeetingMindError

# --- Project path setup ---
# Ensure project root is in sys.path for absolute imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

PROCESSED_AUDIO_DIR = PROJECT_ROOT / "data" / "processed_audio"
PROCESSED_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@handle_errors("Failed to enhance audio")
def enhance_audio(input_file: str, output_file: str = None) -> str:
    """
    Enhance audio quality by reducing background noise.

    Args:
        input_file (str): Path to the input audio file (WAV or other supported formats).
        output_file (str, optional): Path to save the enhanced audio file.
                                    Defaults to (data / processed_audio /{input_file_stem}_clean.wav).

    Returns:
        str: Path to the processed (denoised) audio file.
    """
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"{input_file} not found")

    logging.info(f"Enhancing audio: {input_file}")

    # Load audio
    y, sr = librosa.load(input_path, sr=None)

    # Apply noise reduction
    y_denoised = nr.reduce_noise(y=y, sr=sr)

    # Determine output path
    if output_file is None:
        output_file = PROCESSED_AUDIO_DIR / (input_path.stem + "_clean.wav")
    else:
        output_file = Path(output_file)

    # Save processed audio
    sf.write(output_file, y_denoised, sr)

    logging.info(f"Audio enhancement complete: {output_file}")
    return str(output_file)
