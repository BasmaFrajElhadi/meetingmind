import sys
import os
import logging
from dotenv import load_dotenv
from src.llm.gemini_client import GeminiClient
from src.handlers.error_handler import handle_errors, MeetingMindError
from src.prompt_engineering.templates import load_prompt_template
from src.llm.deepseek_client import DeepSeekV3Client
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- Project path setup ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TopicExtractor:
    """
    TopicExtractor identifies the primary topic or subject of a meeting
    transcript using the DeepSeek-V3 model via OpenRouter API.

    Responsibilities:
    - Format transcript using the "topic_extraction" prompt template.
    - Send request to DeepSeek-V3 via OpenRouter API.
    - Return the extracted topic as a string.
    """

    def __init__(self, client=None):
        """
        Initialize TopicExtractor.

        Args:
            client (optional): Custom LLM client instance (e.g., DeepSeekV3Client). 
                If None, initializes DeepSeekV3Client with API key from environment (OPENROUTER_API_KEY).
        """
        self.parser = StrOutputParser()
        self.prompt_template = load_prompt_template("topic_extraction")
        self.client = client or DeepSeekV3Client(api_key=os.getenv("OPENROUTER_API_KEY"))


    @handle_errors("Failed to extract topic from transcript")
    def extract_topic(self, transcript: str) -> str:
        """
        Extract the main topic from a transcript.

        Args:
            transcript (str): Meeting transcript text.

        Returns:
            str: Extracted topic (stripped of whitespace).
        """
        prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["transcript"]
        )
    
        prompt = prompt.format(transcript=transcript)
        topic = self.client.generate(prompt , self.parser)

        logging.info("Topic extraction completed successfully.")
        return topic.strip()
