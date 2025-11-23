from ..repositories.section_repository import SectionRepository
from ..schemas.section_schema import RefineSectionSchema
from ..utils.exception import (
    DatabaseError,
    ServiceError,
    ResourceNotFoundError,
    LLMError,
)
from .llm_service import LLMService
from ..contracts.section_dto import SectionDTO
from ..models.section_model import Section


class SectionService:
    def __init__(self, section_repo: SectionRepository, llm_service: LLMService):
        self.section_repo = section_repo
        self.llm_service = llm_service

    def refine_section(self, section_id: str, body: RefineSectionSchema) -> SectionDTO:
        try:
            section: Section = self.section_repo.find_by_id(section_id)
            if section is None:
                raise ResourceNotFoundError(
                    message=f"Section with id: {section_id} not found"
                )
            new_content = self.llm_service.refine_section(
                section.project_id,
                section,
                body.user_instruction,
                model_name=body.model_name or "gemini",
            )
            section.content = new_content
            section = self.section_repo.update(section)
            return SectionDTO(
                id=section.id,
                title=section.title,
                content=section.content,
                order=section.order,
                project_id=section.project_id,
            )
        except DatabaseError:
            raise
        except LLMError:
            raise
        except ResourceNotFoundError:
            raise
        except Exception as e:
            raise ServiceError(str(e))
