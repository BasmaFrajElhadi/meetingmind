import requests
import json
from config.config_loader import load_model_config
from src.llm.base_llm_client import BaseLLMClient


class DeepSeekV3Client(BaseLLMClient):
    """
    LLM client implementation using DeepSeek-V3 model via OpenRouter API.

    Responsibilities:
    - Load DeepSeek model configuration from config file.
    - Initialize API client with authentication and model parameters.
    - Generate text responses from prompts.
    - Optionally parse output into structured JSON using an output parser.
    """
    def __init__(self, api_key: str, model_name: str = None, temperature: float = None, max_tokens: int = None):
        """
        Initialize DeepSeekV3Client with a specific DeepSeek model configuration.

        Args:
            api_key (str): API key used to authenticate with OpenRouter API.
            model_name (str, optional): Model name to use. Defaults to config value
                                        or "deepseek/deepseek-chat".
            temperature (float, optional): Sampling temperature for generation.
                                           Defaults to config value or 0.3.
            max_tokens (int, optional): Maximum number of tokens for model output.
                                        Defaults to config value or 1024.
        """
        config = load_model_config().get("deepseek", {})
        
        self.api_key = api_key
        self.model_name = model_name or config.get("model_name", "deepseek/deepseek-chat")
        self.temperature = temperature or config.get("temperature", 0.3)
        self.max_tokens = max_tokens or config.get("max_tokens", 1024)
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def generate(self, prompt: str, output_parser=None, **kwargs) -> str:
        """
        Generate a response from DeepSeek-V3 model.

        Args:
            prompt (str): The input prompt to send to the model.
            output_parser (optional): An object with a `.parse()` method to convert
                                      raw text into structured output (e.g., JSON).
            **kwargs: Additional keyword arguments (reserved for future use).

        Returns:
            str: The model-generated text, optionally parsed via output_parser.

        Raises:
            RuntimeError: If the API response is not successful (HTTP status != 200).
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://yourproject.com",
            "X-Title": "MeetingMind-App"
        }

        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        response = requests.post(self.url, headers=headers, json=payload)

        if response.status_code != 200:
            raise RuntimeError(f"DeepSeek API Error {response.status_code}: {response.text}")

        data = response.json()
        text = data["choices"][0]["message"]["content"]

        if output_parser:
            try:
                return output_parser.parse(text)
            except Exception:
                pass

        return text
