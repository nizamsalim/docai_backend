from ..repositories.user_repository import UserRepository
from ..repositories.project_repository import ProjectRepository
from ..repositories.section_repository import SectionRepository

from ..services.auth_service import AuthService
from ..services.project_service import ProjectService

from ..llm.llm_service import LLMService
from ..llm.context_builder import ContextBuilder
from ..llm.prompt_builder import PromptBuilder


def get_auth_service():
    repo = UserRepository()
    service = AuthService(repo)
    return service


def get_project_service():
    project_repo = ProjectRepository()
    section_repo = SectionRepository()
    prompt_builder = PromptBuilder()
    context_builder = ContextBuilder(project_repo, section_repo)
    llm_service = LLMService(context_builder, prompt_builder)
    service = ProjectService(project_repo, section_repo, llm_service)
    return service
