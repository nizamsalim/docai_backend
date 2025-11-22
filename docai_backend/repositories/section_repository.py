from ..models.section_model import Section
from ..utils.exception import DatabaseError
from ..utils.db import db


class SectionRepository:
    def create(self,section:Section):
        try:
            db.session.add(section)
            db.session.commit()
            return section
        except:
            db.session.rollback()
            raise DatabaseError()