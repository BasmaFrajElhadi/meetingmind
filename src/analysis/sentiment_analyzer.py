import sys
import os
from pathlib import Path
import logging
import json
from dotenv import load_dotenv

from src.prompt_engineering.templates import load_prompt_template
from src.handlers.error_handler import handle_errors, MeetingMindError
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.llm.deepseek_client import DeepSeekV3Client



# Load environment variables
load_dotenv()

# Ensure project root is in sys.path for absolute imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

SENTIMENT_DIR = PROJECT_ROOT / "data" / "analysis_outputs" / "sentiment"
SENTIMENT_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging format and level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SentimentAnalyzer:
    """
    SentimentAnalyzer is responsible for analyzing the emotional tone
    of meeting transcripts using the DeepSeek-V3 model via OpenRouter API.

    It transforms raw meeting text into structured sentiment insights
    that describe the overall emotional state and key emotional signals.

    Responsibilities:
    - Format sentiment analysis prompts using predefined templates.
    - Send transcripts to the LLM (DeepSeekV3Client) for processing.
    - Parse and normalize the AI response into structured sentiment data.
    - Provide actionable sentiment insights (overall sentiment, emotions, scores).
    - Save analysis results to disk in JSON format.
    """
    def __init__(self, client=None):
        """
        Initialize SentimentAnalyzer.

        Args:
            client (optional): Custom LLM client instance (e.g., DeepSeekV3Client). 
                If None, initializes DeepSeekV3Client with API key from environment (OPENROUTER_API_KEY).
        """
        self.parser = JsonOutputParser()
        self.prompt_template = load_prompt_template("sentiment_analysis")
        self.client = client or DeepSeekV3Client(api_key=os.getenv("OPENROUTER_API_KEY"))


    @handle_errors("Failed analyzing sentiment")
    def analyze_sentiment(self, transcript: str) -> dict:
        """
        Analyze the emotional tone and sentiment of a meeting transcript.

        This method sends the transcript to the LLM using a sentiment
        analysis prompt template and attempts to parse the response as JSON.
        If parsing fails, a fallback structure containing the raw text and
        AI output is returned.

        Args:
            transcript (str): Raw meeting transcript text.

        Returns:
            dict: Structured sentiment analysis result. Example:
                {
                    "overall_sentiment": "neutral",
                    "sentiment_score": 0.2,
                    "emotions": ["concern"]
                }

        Raises:
            MeetingMindError:
                If an unexpected error occurs during processing.
        """
        prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["transcript"]
        )
    
        prompt = prompt.format(transcript=transcript)
        text = self.client.generate(prompt=prompt, output_parser=self.parser)

        try:
            sentiment_data  = json.loads(text)
        except Exception :
            sentiment_data = {"text" : transcript , "sentiment": text}

        logging.info("Sentiment analysis complete")
        return sentiment_data
        
    def save_sentiment(self, sentiment_data: dict, output_file: str = None) -> str:
        """
        Save sentiment analysis results to a JSON file.

        Args:
            sentiment_data (dict):
                Sentiment result data.
            output_file (str, optional): Custom file path to save the sentiment file.
                Defaults to: (data/analysis_outputs/sentiment/sentiment.json)

        Returns:
            str:
                Absolute path of the saved JSON file.
        """
        if output_file is None:
            output_file = SENTIMENT_DIR / "sentiment.json"
        else:
            output_file = Path(output_file)

        with open(output_file , "w" , encoding="utf-8") as f:
            json.dump(sentiment_data , f, indent=2 ,  ensure_ascii=False)

        logging.info(f"Sentiment data saved to {output_file}")
        return str(output_file)
    