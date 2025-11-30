from ..llm.context_builder import ContextBuilder
from ..llm.prompt_builder import PromptBuilder
from ..models.project_model import Project
from ..models.section_model import Section
from ..llm.providers import ModelRegistry
from ..utils.exception import LLMError
import json
import re


class LLMService:
    def __init__(self, context_builder: ContextBuilder, prompt_builder: PromptBuilder):
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder

    def __get_provider(self, model_name: str):
        return ModelRegistry.get_provider(model_name)

    def generate_initial_content(
        self, project: Project, section: Section, model_name="gemini"
    ):
        try:
            prompt = self.prompt_builder.get_initial_generation_prompt(
                project.title, project.type, section.title
            )

            provider = self.__get_provider(model_name)
            return provider.generate(prompt)
        except Exception as e:
            raise LLMError(str(e))

    def generate_sections(
        self, project_title: str, project_type: str, model_name="gemini"
    ):
        try:
            prompt = self.prompt_builder.get_initial_sections_generation_prompt(
                project_title, project_type
            )
            provider = self.__get_provider(model_name)
            generated = provider.generate(prompt)
            text = re.sub(r"```[a-zA-Z0-9_-]+\s*([\s\S]*?)```", r"\1", generated)
            return json.loads(text)
        except Exception as e:
            raise LLMError(str(e))

    def refine_section(
        self,
        project_id: str,
        section: Section,
        user_instruction: str,
        context_mode="section",
        model_name="gemini",
    ):
        try:
            context = self.context_builder.build(project_id, section.id, context_mode)

            prompt = self.prompt_builder.get_refinement_prompt(
                section.title, section.content, user_instruction, context
            )

            provider = self.__get_provider(model_name)

            return provider.generate(prompt)
        except Exception as e:
            raise LLMError(str(e))
