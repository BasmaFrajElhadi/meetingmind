from pathlib import Path
import logging
import whisper
import sys
import os

from src.transcription.base_transcriber import BaseTranscriber
from src.transcription.utils import clean_text
from src.handlers.error_handler import handle_errors, MeetingMindError
from config.config_loader import load_model_config

# Ensure project root is in sys.path for absolute imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

TRANSCRIPTS_DIR = PROJECT_ROOT / "data" / "transcripts" 
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

# Logging configuration
logging.basicConfig(level=logging.INFO)


class WhisperTranscriber(BaseTranscriber):
    """
    Transcriber implementation using OpenAI Whisper model.

    Responsibilities:
    - Load Whisper model of specified size.
    - Transcribe audio files to text.
    - Save transcription text to a file.
    """

    def __init__(self):
        """
        Initialize WhisperTranscriber with a specific Whisper model size.
        """
        config = load_model_config()["whisper"]
        model_size = config["model_size"]
        self.model = whisper.load_model(model_size)


    @handle_errors("Failed to convert audio to text")
    def transcribe(self, audio_file: str) -> str:

        """
        Convert an audio file to text using Whisper.

        Args:
            audio_file (str): Path to the audio file.

        Returns:
            str: Cleaned transcription text.
        """

        result = self.model.transcribe(audio_file)
        text = result["text"]
        text = clean_text(text)
        logging.info(f"Transcription complete, length: {len(text)} characters")
        return text

    @handle_errors("Failed to save transcript")
    def save_transcript(self, transcript: str, output_file: str = None) -> str:
        """
        Save transcription text to a file.

        Args:
            transcript (str): Transcribed text.
            output_file (str, optional): Path to save transcript. Defaults to TRANSCRIPTS_DIR/transcript.txt.

        Returns:
            str: Path to the saved transcript file.
        """
        if output_file is None:
            output_file = TRANSCRIPTS_DIR / "transcript.txt"
        else:
            output_file = Path(output_file)

        output_file.write_text(transcript, encoding="utf-8")
        logging.info(f"Transcript saved to {output_file}")
        return str(output_file)
