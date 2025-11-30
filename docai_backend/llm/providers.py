from abc import ABC, abstractmethod
from langchain_google_genai import ChatGoogleGenerativeAI as GeminiClient
from langchain_xai import ChatXAI as GrokClient
from langchain_groq import ChatGroq as GroqClient
import os


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class GeminiProvider(LLMProvider):
    def __init__(self, model_name="gemini-2.5-flash", temperature=0.5):
        self.model = GeminiClient(
            model=model_name,
            temperature=temperature,
            api_key=os.getenv("GEMINI_API_KEY"),
        )

    def generate(self, prompt: str) -> str:
        res = self.model.invoke(prompt)
        return res.content


class LlamaProvider(LLMProvider):
    def __init__(self, model_name="llama-3.3-70b-versatile", temperature=0.6):
        self.model = GroqClient(
            model=model_name, temperature=temperature, api_key=os.getenv("GROQ_API_KEY")
        )

    def generate(self, prompt: str) -> str:
        res = self.model.invoke(prompt)
        return res.content


class GPTProvider(LLMProvider):
    def __init__(self, model_name="openai/gpt-oss-120b", temperature=0.6):
        self.model = GroqClient(
            model=model_name, temperature=temperature, api_key=os.getenv("GROQ_API_KEY")
        )

    def generate(self, prompt: str) -> str:
        res = self.model.invoke(prompt)
        return res.content


class ModelRegistry:
    MODELS = {
        "gemini": GeminiProvider,
        "llama": LlamaProvider,
        "gpt": GPTProvider,
    }

    @staticmethod
    def get_provider(model_name="gemini"):
        if model_name not in ModelRegistry.MODELS.keys():
            raise ValueError(f"Model '{model_name}' could not be found")
        return ModelRegistry.MODELS[model_name]()
