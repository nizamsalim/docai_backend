from ..models.refinement_model import Refinement
from ..utils.exception import DatabaseError
from ..utils.db import db
from sqlalchemy.exc import SQLAlchemyError


class RefinementRepository:
    def create(self, refinement: Refinement):
        try:
            db.session.add(refinement)
            db.session.commit()
            return refinement
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(str(e))

    def update(self, refinement: Refinement):
        try:
            db.session.commit()
            return refinement
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(str(e))

    def find_by_id(self, section_id: str) -> Refinement | None:
        try:
            section = db.session.execute(
                db.select(Refinement).filter(Refinement.id == section_id)
            ).scalar_one_or_none()
            return section
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))
