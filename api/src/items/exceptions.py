from src.exceptions import BadRequest


class ItemNotFound(BadRequest):
    DETAIL = "Item not found."

class ItemAlreadyExists(BadRequest):
    DETAIL = "Item already exists."
