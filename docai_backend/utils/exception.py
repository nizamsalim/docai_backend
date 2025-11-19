class BaseAppException(Exception):
    status_code = 500

    def __init__(self, message=None, data=None,error_code=None):
        super().__init__(message)
        self.message = message or "An unexpected error occurred."
        self.data = data or {}
        self.error_code = error_code

class ValidationError(BaseAppException):
    status_code = 422
    def __init__(self,data=None,message="Input validation failed",code="VALIDATION_ERROR"):
        super().__init__(message,data,code)

class DatabaseError(BaseAppException):
    status_code = 500
    def __init__(self,data=None,message="An unknown database error occured",code="DATABASE_ERROR"):
        super().__init__(message,data,code)

class UserExistsError(BaseAppException):
    status_code = 409
    def __init__(self,data=None,message="Username already exists",code="USER_EXISTS"):
        super().__init__(message,data,code)

class ServiceError(BaseAppException):
    status_code = 500
    def __init__(self,data=None,message="An unknown error occured",code="SERVICE_ERROR"):
        super().__init__(message,data,code)

class InvalidCredentialsError(BaseAppException):
    status_code = 401
    def __init__(self,data=None,message="Invalid login credentials",code="INVALID_CREDENTIALS_ERROR"):
        super().__init__(message,data,code)


