from src.exceptions import EntityNotFound, BadRequest


class OrderNotFound(EntityNotFound):
    DETAIL = "Order not found."

class OrderAlreadyFinished(BadRequest):
    DETAIl = "Order already finished."
