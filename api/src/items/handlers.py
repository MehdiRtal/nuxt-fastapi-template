from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from src.items.repository import ItemsRepository
from src.items.service import ItemsService


@local_handler.register(event_name="*")
async def handle_all_events(event: Event):
    event_name, payload = event
    items_repository = ItemsRepository(payload)
    items_service = ItemsService(items_repository)
    return items_service
