from ..models.user_model import User
from ..utils.db import db
from ..utils.exception import DatabaseError
class UserRepository:
    def find_by_username(self,username:str) -> User|None :
        try:
            user:User|None = db.session.execute(
                db.select(User).filter(User.username == username)
            ).scalar_one_or_none()
            return user
        except:
            raise DatabaseError()
    
    def create(self,user:User):
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except:
            db.session.rollback()
            raise DatabaseError()