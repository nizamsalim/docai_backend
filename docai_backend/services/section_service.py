from ..repositories.section_repository import SectionRepository
from ..repositories.refinement_repository import RefinementRepository
from ..repositories.comment_repository import CommentRepository
from ..schemas.section_schema import (
    RefineSectionSchema,
    UpdateSectionSchema,
    CommentSchema,
)
from ..utils.exception import (
    DatabaseError,
    ServiceError,
    ResourceNotFoundError,
    LLMError,
)
from .llm_service import LLMService
from ..contracts.section_dto import SectionDTO, RefinementDTO, CommentDTO
from ..models.section_model import Section
from ..models.refinement_model import Refinement
from ..models.comment_model import Comment


class SectionService:
    def __init__(
        self,
        section_repo: SectionRepository,
        refinement_repo: RefinementRepository,
        comment_repo: CommentRepository,
        llm_service: LLMService,
    ):
        self.section_repo = section_repo
        self.refinement_repo = refinement_repo
        self.comment_repo = comment_repo
        self.llm_service = llm_service

    def refine_section(self, section_id: str, body: RefineSectionSchema) -> SectionDTO:
        try:
            section: Section = self.section_repo.find_by_id(section_id)
            if section is None:
                raise ResourceNotFoundError(
                    message=f"Section with id: {section_id} not found"
                )
            before_content = section.content
            new_content = self.llm_service.refine_section(
                section.project_id,
                section,
                body.user_instruction,
                model_name=body.model_name or "gemini",
            )
            section.content = new_content
            section = self.section_repo.update(section)

            refinement = Refinement(
                prompt=body.user_instruction,
                section_id=section.id,
                before_content=before_content,
                after_content=new_content,
            )
            self.refinement_repo.create(refinement)

            return SectionDTO(
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
                        before_content=r.before_content,
                        after_content=r.after_content,
                    )
                    for r in list(section.refinements)[::-1]
                ],
                comments=[
                    CommentDTO(id=c.id, section_id=c.section_id, content=c.content)
                    for c in section.comments
                ],
            )
        except DatabaseError:
            raise
        except LLMError:
            raise
        except ResourceNotFoundError:
            raise
        except Exception as e:
            raise ServiceError(str(e))

    def update_section(self, section_id: str, body: UpdateSectionSchema):
        try:
            section = self.section_repo.find_by_id(section_id)
            if section is None:
                raise ResourceNotFoundError(
                    message=f"Section with id: {section_id} not found."
                )
            if body.title:
                section.title = body.title
            if body.content:
                section.content = body.content
            section = self.section_repo.update(section)
            return SectionDTO(
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
                        before_content=r.before_content,
                        after_content=r.after_content,
                    )
                    for r in list(section.refinements)[::-1]
                ],
                comments=[
                    CommentDTO(id=c.id, section_id=c.section_id, content=c.content)
                    for c in section.comments
                ],
            )
        except DatabaseError:
            raise
        except ResourceNotFoundError:
            raise
        except Exception as e:
            raise ServiceError(str(e))

    def add_section_comment(self, section_id: str, body: CommentSchema) -> CommentDTO:
        try:
            section = self.section_repo.find_by_id(section_id)
            if section is None:
                raise ResourceNotFoundError(
                    f"Section with id: {section_id} could not be found"
                )
            comment = Comment(content=body.content, section_id=section_id)
            comment = self.comment_repo.create(comment)
            return CommentDTO(
                id=comment.id, section_id=comment.section_id, content=comment.content
            )
        except DatabaseError:
            raise
        except ResourceNotFoundError:
            raise
        except Exception as e:
            raise ServiceError(str(e))

    def update_section_comment(
        self, section_id: str, comment_id: str, body: CommentSchema
    ):
        try:
            pass
        except DatabaseError:
            raise
        except ResourceNotFoundError:
            raise
        except Exception as e:
            raise ServiceError(str(e))
