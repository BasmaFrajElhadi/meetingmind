from abc import ABC, abstractmethod
from pathlib import Path

class BaseTranscriber(ABC):
    """
    Abstract base class for all transcribers.

    Defines the interface that any concrete transcriber implementation must follow.
    """

    @abstractmethod
    def transcribe(self, audio_file: str) -> str:
        """
        Transcribe an audio file into text.

        Args:
            audio_file (str): Path to the audio file.

        Returns:
            str: Transcribed text.
        """
        pass

    @abstractmethod
    def save_transcript(self, transcript: str, output_file: str = None) -> str:
        """
        Save a transcription text to a file.

        Args:
            transcript (str): The text obtained from transcription.
            output_file (str, optional): Path to save the transcript. Defaults to a standard directory.

        Returns:
            str: Path to the saved transcript file.
        """
        pass
