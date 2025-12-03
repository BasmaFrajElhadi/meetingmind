import sys
import os
from pathlib import Path
import logging
from dotenv import load_dotenv

from src.prompt_engineering.templates import load_prompt_template
from src.handlers.error_handler import handle_errors, MeetingMindError
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.llm.deepseek_client import DeepSeekV3Client


# Load environment variables from .env
load_dotenv()

# Ensure project root is available for imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


SUMMARIES_DIR = PROJECT_ROOT / "data" / "analysis_outputs" / "summaries"
SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class MeetingSummarizer:
    """
    MeetingSummarizer generates concise and structured summaries
    from raw meeting transcripts using the DeepSeek-V3 model
    via OpenRouter API.

    Responsibilities:
    - Generate structured summaries from transcripts.
    - Use prompt templates to guide the summarization process.
    - Interface with DeepSeekV3Client for AI-powered summarization.
    - Store summaries as text files for later reference.
    """

    def __init__(self, client=None):
        """
        Initialize the MeetingSummarizer.

        Args:
            client (optional): Custom LLM client instance (e.g., DeepSeekV3Client). 
                If None, initializes DeepSeekV3Client with API key from environment (OPENROUTER_API_KEY).
        """
        self.parser = StrOutputParser()
        self.prompt_template = load_prompt_template("summarization")
        self.client = client or DeepSeekV3Client(api_key=os.getenv("OPENROUTER_API_KEY"))


    @handle_errors("Failed to summarize transcript")
    def summarize(self, transcript: str) -> str:
        """
        Generate a structured summary for a meeting transcript using LangChain.

        Args:
            transcript (str): Full meeting transcript.

        Returns:
            str: AI-generated summary in structured bullet format.

        Raises:
            MeetingMindError: If summarization fails unexpectedly.
        """

        prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["transcript"]
        )
    
        prompt = prompt.format(transcript=transcript)
        summary = self.client.generate(prompt , self.parser)
        
        logging.info("Summary generated successfully")
        return summary

    def save_summary(self, summary: str, output_file: str = None) -> str:
        """
        Save the summary text to a file.

        Args:
            summary (str): Generated summary content.

            output_file (str, optional): Custom output path.
                Defaults to: (data/analysis_outputs/summaries/summary.txt)

        Returns:
            str:
                Absolute path to the saved summary file.
        """
        output_path = Path(output_file) if output_file else SUMMARIES_DIR / "summary.txt"
        output_path.write_text(summary, encoding="utf-8")

        logging.info(f"Summary saved to {output_path}")
        return str(output_path)
