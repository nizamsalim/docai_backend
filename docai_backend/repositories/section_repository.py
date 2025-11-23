from ..models.section_model import Section
from ..utils.exception import DatabaseError
from ..utils.db import db
from sqlalchemy.exc import SQLAlchemyError


class SectionRepository:
    def create(self, section: Section):
        try:
            db.session.add(section)
            db.session.commit()
            return section
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(str(e))

    def update(self, section: Section):
        try:
            db.session.commit()
            return section
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(str(e))

    def create_many(self, sections: list[Section]):
        try:
            db.session.add_all(sections)
            db.session.commit()
            return sections
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(str(e))

    def find_by_id(self, section_id: str) -> Section | None:
        try:
            section = db.session.execute(
                db.select(Section).filter(Section.id == section_id)
            ).scalar_one_or_none()
            return section
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))
