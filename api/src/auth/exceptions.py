from src.exceptions import Unauthorized, Forbidden


class InvalidAccessToken(Unauthorized):
    DETAIL = "Invalid access token."

class InvalidVerifyToken(Unauthorized):
    DETAIL = "Invalid verify token."

class InvalidCredentials(Unauthorized):
    DETAIL = "Invalid credentials."

class PermissionRequired(Forbidden):
    DETAIL = "Permission required."
