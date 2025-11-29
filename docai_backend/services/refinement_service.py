from ..repositories.refinement_repository import RefinementRepository
from ..repositories.section_repository import SectionRepository
from ..utils.exception import ResourceNotFoundError, DatabaseError, ServiceError
from ..models.refinement_model import Refinement
from ..contracts.section_dto import RefinementDTO


class RefinementService:
    def __init__(
        self, refinement_repo: RefinementRepository, section_repo: SectionRepository
    ):
        self.refinement_repo = refinement_repo
        self.section_repo = section_repo

    def rate_refinement(self, refinement_id: str, rating: str) -> RefinementDTO:
        try:
            refinement: Refinement = self.refinement_repo.find_by_id(refinement_id)
            if refinement is None:
                raise ResourceNotFoundError(
                    f"Refinement with id: {refinement_id} could not be found"
                )
            refinement.rating = rating
            refinement = self.refinement_repo.update(refinement)

            return RefinementDTO(
                id=refinement.id,
                prompt=refinement.prompt,
                rating=refinement.rating,
                section_id=refinement.section_id,
                before_content=refinement.before_content,
                after_content=refinement.after_content,
            )

        except ResourceNotFoundError:
            raise
        except DatabaseError:
            raise
        except Exception as e:
            raise ServiceError(str(e))
