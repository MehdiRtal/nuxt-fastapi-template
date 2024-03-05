from src.exceptions import EntityNotFound, EntityAlreadyExists


class ItemNotFound(EntityNotFound):
    DETAIL = "Item not found."

class ItemAlreadyExists(EntityAlreadyExists):
    DETAIL = "Item already exists."
