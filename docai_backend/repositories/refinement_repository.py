from ..models.refinement_model import Refinement
from ..utils.exception import DatabaseError
from ..utils.db import db


class RefinementRepository:
    def create(self, refinement: Refinement):
        try:
            db.session.add(refinement)
            db.session.commit()
            return refinement
        except:
            db.session.rollback()
            raise DatabaseError()
