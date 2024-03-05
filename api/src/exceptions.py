from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Internal server error."

    def __init__(self, **kwargs):
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)

class Forbidden(CustomHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Forbidden."

class NotFound(CustomHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Not found."

class BadRequest(CustomHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request."

class Unauthorized(CustomHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Unauthorized."

    def __init__(self):
        super().__init__(headers={"WWW-Authenticate": "Bearer"})

class EntityNotFound(BadRequest):
    pass

class EntityAlreadyExists(BadRequest):
    pass
