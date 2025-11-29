from ..models.comment_model import Comment
from ..utils.exception import DatabaseError
from ..utils.db import db


class CommentRepository:
    def create(self, comment: Comment):
        try:
            db.session.add(comment)
            db.session.commit()
            return comment
        except:
            db.session.rollback()
            raise DatabaseError()

    def update(self, comment: Comment):
        try:
            db.session.commit()
            return comment
        except:
            db.session.rollback()
            raise DatabaseError()

    def delete(self, comment: Comment):
        try:
            db.session.delete(comment)
            db.session.commit()
        except:
            db.session.rollback()
            raise DatabaseError()

    def find_by_id(self, comment_id: str) -> Comment | None:
        try:
            comment = db.session.execute(
                db.select(Comment).filter(Comment.id == comment_id)
            ).scalar_one_or_none()
            return comment
        except Exception as e:
            raise DatabaseError(str(e))
