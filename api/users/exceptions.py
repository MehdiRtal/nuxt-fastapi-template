from exceptions import BadRequest


class UserNotFound(BadRequest):
    DETAIL = "User not found."

class UserAlreadyExists(BadRequest):
    DETAIL = "User already exists."

class UserNotActive(BadRequest):
    DETAIL = "User not active."

class UserNotVerified(BadRequest):
    DETAIL = "User not verified."
