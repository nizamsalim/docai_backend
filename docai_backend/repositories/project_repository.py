from ..models.project_model import Project
from ..utils.db import db
from ..utils.exception import DatabaseError
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError


class ProjectRepository:
    def create(self, project: Project):
        try:
            db.session.add(project)
            db.session.commit()
            return project
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(str(e))

    def update(self, project: Project):
        try:
            db.session.commit()
            return project
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(str(e))

    def find_all(self) -> list[Project]:
        try:
            result = db.session.execute(
                db.select(Project).order_by(Project.accessed_at.desc())
            ).scalars()
            return result
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))

    def find_by_id(self, project_id: str) -> Project | None:
        try:
            query = (
                db.select(Project)
                .options(joinedload(Project.sections))
                .filter(Project.id == project_id)
            )

            project = db.session.execute(query).unique().scalar_one_or_none()
            return project
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))
