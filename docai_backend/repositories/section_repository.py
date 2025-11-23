from ..models.section_model import Section
from ..utils.exception import DatabaseError
from ..utils.db import db


class SectionRepository:
    def create(self, section: Section):
        try:
            db.session.add(section)
            db.session.commit()
            return section
        except:
            db.session.rollback()
            raise DatabaseError()

    def create_many(self, sections: list[Section]):
        try:
            db.session.add_all(sections)
            db.session.commit()
            return sections
        except:
            db.session.rollback()
            raise DatabaseError()

    def find_by_id(self, section_id: str) -> Section | None:
        try:
            section = db.session.execute(
                db.select(Section).filter_by(Section.id == section_id)
            ).scalar_one_or_none()
            return section
        except:
            raise DatabaseError()
