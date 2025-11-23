from abc import ABC, abstractmethod
from langchain_google_genai import ChatGoogleGenerativeAI
import os


class LLMProvider(ABC):
    def generate(self, prompt: str) -> str:
        pass


class GeminiProvider(LLMProvider):
    def __init__(self, model_name="gemini-2.5-flash", temperature=0.5):
        self.model = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            api_key=os.getenv("GEMINI_API_KEY"),
        )

    def generate(self, prompt: str) -> str:
        res = self.model.invoke(prompt)
        return res.content


class ModelRegistry:
    MODELS = {"gemini": GeminiProvider}

    @staticmethod
    def get_provider(model_name="gemini"):
        return ModelRegistry.MODELS[model_name]()
