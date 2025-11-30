from ..models.comment_model import Comment
from ..utils.exception import DatabaseError
from ..utils.db import db
from sqlalchemy.exc import SQLAlchemyError


class CommentRepository:
    def create(self, comment: Comment):
        try:
            db.session.add(comment)
            db.session.commit()
            return comment
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(str(e))

    def update(self, comment: Comment):
        try:
            db.session.commit()
            return comment
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(str(e))

    def delete(self, comment: Comment):
        try:
            db.session.delete(comment)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(str(e))

    def find_by_id(self, comment_id: str) -> Comment | None:
        try:
            comment = db.session.execute(
                db.select(Comment).filter(Comment.id == comment_id)
            ).scalar_one_or_none()
            return comment
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))
