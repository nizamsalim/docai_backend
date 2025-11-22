from ..repositories.user_repository import UserRepository
from ..repositories.project_repository import ProjectRepository
from ..repositories.section_repository import SectionRepository

from ..services.auth_service import AuthService
from ..services.project_service import ProjectService

def get_auth_service():
    repo = UserRepository()
    service = AuthService(repo)
    return service

def get_project_service():
    project_repo = ProjectRepository()
    section_repo = SectionRepository()
    service = ProjectService(project_repo,section_repo)
    return service