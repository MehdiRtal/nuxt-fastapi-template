from api.exceptions import BadRequest


class UserNotFound(BadRequest):
    DETAIL = "User not found."

class UserAlreadyExists(BadRequest):
    DETAIL = "User already exists."

class UserNotActive(BadRequest):
    DETAIL = "User not active."

class UserNotVerified(BadRequest):
    DETAIL = "User not verified."

class UserAlreadyVerified(BadRequest):
    DETAIL = "User already verified."

class UserOAuthNotLinked(BadRequest):
    DETAIL = "User OAuth not linked."
