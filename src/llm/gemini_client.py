from abc import ABC
import google.generativeai as genai

from config.config_loader import load_model_config
from src.llm.base_llm_client import BaseLLMClient


class GeminiClient(BaseLLMClient):
    """
    LLM client implementation using Google Gemini model.

    Responsibilities:
    - Load Gemini model configuration from config file.
    - Initialize and configure Gemini Generative AI client.
    - Generate text responses from prompts.
    """

    def __init__(self, api_key: str, json_output: bool = False):
        """
        Initialize GeminiClient with a specific Gemini model configuration.

        Args:
            api_key (str): API key used to authenticate with Google Gemini.
            json_output (bool, optional): Whether the response should be returned
                                          in JSON format. Defaults to False.
        """
        config = load_model_config()["gemini"]
        genai.configure(api_key=api_key)

        model_name = config["model_name"]
        generation_config = config["generation"]

        if json_output or config.get("json_output", False):
            generation_config["response_mime_type"] = "application/json"

        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config
        )

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a chat response from the Gemini LLM.

        Args:
            prompt (str): The input prompt to send to the model.

        Returns:
            object: The raw response object from Gemini containing the generated content.
        """
        response = self.model.generate_content(prompt)
        return response.text
