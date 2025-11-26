from ..repositories.user_repository import UserRepository
from ..schemas.auth_schema import RegisterSchema, LoginSchema
from ..utils.exception import (
    UserExistsError,
    ServiceError,
    InvalidCredentialsError,
    InvalidAccessTokenError,
    MissingAccessTokenError,
    DatabaseError,
)
from ..models.user_model import User
from ..contracts.user_dto import UserDTO
from werkzeug.security import (
    generate_password_hash as create_hash,
    check_password_hash as check_password,
)
from ..utils.jwt import JWTProvider


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, user: RegisterSchema) -> tuple[UserDTO, str]:
        try:
            user_exists = self.repo.find_by_username(user.username)
            if user_exists:
                raise UserExistsError(
                    message=f"User with username '{user.username}' already exists"
                )

            new_user = User(
                name=user.name,
                password=create_hash(user.password),
                username=user.username,
            )
            new_user = self.repo.create(new_user)
            return UserDTO(
                name=new_user.name,
                username=new_user.username,
                id=new_user.id,
            ), JWTProvider.create_token(new_user.id)

        except UserExistsError:
            raise
        except:
            raise ServiceError()

    def login_user(self, user: LoginSchema) -> tuple[UserDTO, str]:
        try:
            db_user = self.repo.find_by_username(user.username)
            if db_user is None:
                raise InvalidCredentialsError()
            if not check_password(db_user.password, user.password):
                raise InvalidCredentialsError()
            return UserDTO(
                name=db_user.name,
                username=db_user.username,
                id=db_user.id,
            ), JWTProvider.create_token(db_user.id)
        except InvalidCredentialsError:
            raise
        except DatabaseError:
            raise
        except Exception as e:
            print(str(e))
            raise ServiceError()

    def validate_user(self, access_token: str) -> UserDTO:
        try:
            payload = JWTProvider.decode_token(access_token)
            user = self.repo.find_by_id(payload["id"])
            if user is None:
                raise InvalidAccessTokenError
            return UserDTO(
                name=user.name,
                username=user.username,
                id=user.id,
            )
        except InvalidAccessTokenError:
            raise
        except MissingAccessTokenError:
            raise
        except Exception as e:
            print(str(e))
            raise ServiceError()
