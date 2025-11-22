from ..models.project_model import Project
from ..utils.db import db
from ..utils.exception import DatabaseError
from sqlalchemy.orm import joinedload


class ProjectRepository:
    def create(self, project: Project):
        try:
            db.session.add(project)
            db.session.commit()
            return project
        except:
            db.session.rollback()
            raise DatabaseError()

    def find_all(self) -> list[Project]:
        try:
            result = db.session.execute(db.select(Project)).scalars()
            return result
        except Exception as e:
            # Log if needed
            print(str(e))

            raise DatabaseError()

    def find_by_id(self, project_id: str) -> Project | None:
        try:
            query = (
                db.select(Project)
                .options(joinedload(Project.sections))
                .filter(Project.id == project_id)
            )

            project = db.session.execute(query).unique().scalar_one_or_none()
            return project
        except Exception as e:
            raise DatabaseError(str(e))
