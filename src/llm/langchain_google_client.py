from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from config.config_loader import load_model_config
from src.llm.base_llm_client import BaseLLMClient

class LangChainGoogleClient(BaseLLMClient):
    """
    LLM client implementation using Google Generative AI via LangChain.

    Responsibilities:
    - Load model configuration from the config file.
    - Initialize and configure the GoogleGenerativeAI client.
    - Generate text responses from prompts using LangChain's modern Runnable API.
    - Optionally parse output using a provided parser.
    """
    def __init__(self, api_key: str):
        """
        Initialize LangChainGoogleClient with a specific model configuration.

        Args:
            api_key (str): API key used to authenticate with Google Generative AI.
        """
        config = load_model_config()["gemini"]
        model_name = config["model_name"]

        generation_config = config["generation"]

        self.model = GoogleGenerativeAI(
            api_key=api_key,
            model=model_name,
            **generation_config
        )

    def generate(self, prompt,output_parser=None, **kwargs) -> str:
        """
        Generate text from the LLM using a prompt.
        
        Args:
            prompt (str): Input prompt to send to the model.
            output_parser (optional): An output parser object with a `.parse()`
                                      method to format the model output.
            **kwargs: Additional keyword arguments passed to the LLM invocation.

        Returns:
            str: Generated text from the LLM, optionally parsed.
        """
        prompt_template = PromptTemplate.from_template("{input}")

        result = (prompt_template | self.model).invoke({"input": prompt}, **kwargs)

        # Parse output if parser is provided
        if output_parser:
            result = output_parser.parse(result)

        return result

     