from ..repositories.project_repository import ProjectRepository
from ..repositories.section_repository import SectionRepository
from ..schemas.project_schema import CreateProjectSchema as ProjectSchema
from ..utils.exception import ServiceError, DatabaseError, ResourceNotFoundError
from ..models.project_model import Project
from ..models.section_model import Section
from ..contracts.project_dto import ProjectDTO, SectionDTO


class ProjectService:
    def __init__(
        self, project_repo: ProjectRepository, section_repo: SectionRepository
    ):
        self.project_repo = project_repo
        self.section_repo = section_repo

    def create_project(self, project: ProjectSchema):
        project_id = None
        try:
            # create project
            new_project = Project(
                title=project.title,
                type=project.type,
                section_count=len(project.sections),
            )
            new_project = self.project_repo.create(new_project)

            project_id = new_project.id

            for section in project.sections:
                new_section = Section(
                    title=section.title, order=section.order, project_id=project_id
                )
                self.section_repo.create(new_section)

            # create sections
            return ProjectDTO(
                id=new_project.id,
                title=new_project.title,
                type=new_project.type,
                section_count=new_project.section_count,
                created_at=new_project.created_at,
                updated_at=new_project.updated_at,
            )
        except DatabaseError:
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
