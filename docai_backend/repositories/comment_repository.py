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
