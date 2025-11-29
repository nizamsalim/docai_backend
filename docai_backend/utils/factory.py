from ..repositories.user_repository import UserRepository
from ..repositories.project_repository import ProjectRepository
from ..repositories.section_repository import SectionRepository
from ..repositories.refinement_repository import RefinementRepository
from ..repositories.comment_repository import CommentRepository

from ..services.auth_service import AuthService
from ..services.project_service import ProjectService
from ..services.section_service import SectionService
from ..services.refinement_service import RefinementService

from ..services.llm_service import LLMService
from ..llm.context_builder import ContextBuilder
from ..llm.prompt_builder import PromptBuilder


def get_auth_service():
    repo = UserRepository()
    service = AuthService(repo)
    return service


def get_llm_service():
    project_repo = ProjectRepository()
    section_repo = SectionRepository()
    prompt_builder = PromptBuilder()
    context_builder = ContextBuilder(project_repo, section_repo)
    llm_service = LLMService(context_builder, prompt_builder)
    return llm_service


def get_project_service():
    project_repo = ProjectRepository()
    section_repo = SectionRepository()
    llm_service = get_llm_service()
    service = ProjectService(project_repo, section_repo, llm_service)
    return service


def get_section_service():
    section_repo = SectionRepository()
    refinement_repo = RefinementRepository()
    comment_repo = CommentRepository()
    llm_service = get_llm_service()
    service = SectionService(section_repo, refinement_repo, comment_repo, llm_service)
    return service


def get_refinement_service():
    refinement_repo = RefinementRepository()
    section_repo = SectionRepository()
    service = RefinementService(refinement_repo, section_repo)
    return service
