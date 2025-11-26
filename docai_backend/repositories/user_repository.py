from ..models.user_model import User
from ..utils.db import db
from ..utils.exception import DatabaseError


class UserRepository:
    def find_by_username(self, username: str) -> User | None:
        try:
            user: User | None = db.session.execute(
                db.select(User).filter(User.username == username)
            ).scalar_one_or_none()
            return user
        except Exception as e:
            raise DatabaseError(str(e))

    def find_by_id(self, id: str) -> User | None:
        try:
            user: User | None = db.session.execute(
                db.select(User).filter(User.id == id)
            ).scalar_one_or_none()
            return user
        except Exception as e:
            raise DatabaseError(str(e))

    def create(self, user: User):
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(str(e))
