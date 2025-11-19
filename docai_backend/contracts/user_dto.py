from dataclasses import dataclass as dc
from datetime import datetime

@dc
class UserDTO:
    name:str
    username:str
    id:str

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "username":self.username,
        }