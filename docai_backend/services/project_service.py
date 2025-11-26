from ..repositories.project_repository import ProjectRepository
from ..repositories.section_repository import SectionRepository
from .llm_service import LLMService
from ..schemas.project_schema import (
    CreateProjectSchema as ProjectSchema,
    UpdateProjectSchema,
)
from ..utils.exception import (
    ServiceError,
    DatabaseError,
    ResourceNotFoundError,
    LLMError,
)
from ..models.project_model import Project
from ..models.section_model import Section
from ..contracts.project_dto import ProjectDTO
from ..contracts.section_dto import RefinementDTO, SectionDTO


class ProjectService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        section_repo: SectionRepository,
        llm_service: LLMService,
    ):
        self.project_repo = project_repo
        self.section_repo = section_repo
        self.llm_service = llm_service

    def create_project(self, project: ProjectSchema) -> ProjectDTO:
        project_id = None
        try:
            # create project
            new_project = Project(
                title=project.title,
                type=project.type,
                section_count=len(project.sections),
            )
            new_project = self.project_repo.create(new_project)
            print("Project created")

            project_id = new_project.id

            new_sections: list[Section] = []
            for i, section in enumerate(project.sections):
                new_section = Section(
                    title=section.title, order=section.order, project_id=project_id
                )
                content = self.llm_service.generate_initial_content(
                    new_project, new_section
                )
                print(f"Section {i+1} generated")
                new_section.content = content
                new_sections.append(new_section)
            self.section_repo.create_many(new_sections)

            # create sections
            return ProjectDTO(
                id=new_project.id,
                title=new_project.title,
                type=new_project.type,
                section_count=new_project.section_count,
                created_at=new_project.created_at,
                updated_at=new_project.updated_at,
                sections=[
                    SectionDTO(
                        id=section.id,
                        title=section.title,
                        content=section.content,
                        order=section.order,
                        project_id=section.project_id,
                        refinements=[
                            RefinementDTO(
                                id=r.id,
                                prompt=r.prompt,
                                rating=r.rating,
                                section_id=r.section_id,
                            )
                            for r in section.refinements
                        ],
                    )
                    for section in new_project.sections
                ],
            )
        except DatabaseError:
            raise
        except LLMError:
            raise
        except Exception as e:
            print(str(e))
            raise ServiceError()

    def get_all_projects(self) -> list[ProjectDTO]:
        try:
            res: list[Project] = self.project_repo.find_all()
            return [
                ProjectDTO(
                    id=p.id,
                    title=p.title,
                    type=p.type,
                    section_count=p.section_count,
                    created_at=p.created_at,
                    updated_at=p.updated_at,
                )
                for p in res
            ]
        except DatabaseError:
            raise
        except Exception as e:

            raise ServiceError(str(e))

    def get_project_data(self, project_id: str) -> ProjectDTO:
        try:
            project: Project | None = self.project_repo.find_by_id(project_id)
            if project is None:
                raise ResourceNotFoundError(
                    message=f"Project with id: {project_id} could not be found"
                )
            return ProjectDTO(
                id=project.id,
                title=project.title,
                type=project.type,
                section_count=project.section_count,
                created_at=project.created_at,
                updated_at=project.updated_at,
                sections=[
                    SectionDTO(
                        id=section.id,
                        title=section.title,
                        content=section.content,
                        order=section.order,
                        project_id=section.project_id,
                        refinements=[
                            RefinementDTO(
                                id=r.id,
                                prompt=r.prompt,
                                rating=r.rating,
                                section_id=r.section_id,
                            )
                            for r in section.refinements
                        ],
                    )
                    for section in project.sections
                ],
            )
        except DatabaseError:
            raise
        except ResourceNotFoundError:
            raise
        except Exception as e:
            raise ServiceError(str(e))

    def update_project(self, project_id: str, body: UpdateProjectSchema):
        try:
            project = self.project_repo.find_by_id(project_id)
            if project is None:
                raise ResourceNotFoundError(
                    message=f"Project with id: {project_id} not found"
                )
            project.title = body.title
            project: Project = self.project_repo.update(project)
            return ProjectDTO(
                id=project.id,
                title=project.title,
                type=project.type,
                section_count=project.section_count,
                created_at=project.created_at,
                updated_at=project.updated_at,
            )
        except DatabaseError:
            raise
        except ResourceNotFoundError:
            raise
        except Exception as e:
            raise ServiceError(str(e))

    def test_llm(self, project_id: str):
        project = self.project_repo.find_by_id(project_id)
        section = project.sections[0]
        res = self.llm_service.generate_initial_content(project, section, "gemini")
        print(res)
        return res
