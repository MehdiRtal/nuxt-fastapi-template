from fastapi import APIRouter, Depends, Request
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from src.db import DBSession
from src.auth.utils import pwd_context, google_oauth_client
from src.auth.dependencies import CurrentUser
from src.items.models import Item, ItemCreate, ItemRead, ItemUpdate
from src.items.exceptions import ItemNotFound
from src.auth.dependencies import require_superuser
from src.auth.exceptions import InvalidCredentials
from src.models import DefaultResponse

from src.users.models import User, UserCreate, UserRead, UserUpdate
from src.users.dependencies import valid_sellix_signature
from src.users.exceptions import UserNotFound, UserAlreadyExists, UserOAuthNotLinked
from src.users.utils import create_payment


router = APIRouter(tags=["Users"], prefix="/users")

@router.post("/me/change-password")
async def change_current_user_password(db: DBSession, current_user: CurrentUser, current_password: str, new_password: str) -> UserRead:
    if not pwd_context.verify(current_password, current_user.password):
        raise InvalidCredentials()
    current_user.password = pwd_context.hash(new_password)
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.post("/me/unlink/google")
async def unlink_current_user_google(db: DBSession, current_user: CurrentUser) -> UserRead:
    if not current_user.google_oauth_refresh_token:
        raise UserOAuthNotLinked()
    await google_oauth_client.revoke_token(current_user.google_oauth_refresh_token, "refresh_token")
    current_user.google_oauth_refresh_token = None
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.post("/me/payment")
async def add_current_user_payment(request: Request, current_user: CurrentUser, value: float) -> dict:
    callback_url = request.url_for("current_user_payment_callback")
    payment = create_payment(value, current_user.email, {"user_id": current_user.id}, callback_url)
    return {"payment_url": payment["data"]["url"]}

@router.get("/me/payment/callback", dependencies=[Depends(valid_sellix_signature)])
async def current_user_payment_callback(request: Request, db: DBSession) -> DefaultResponse:
    body = await request.json()
    db_user = await db.get(User, body["data"]["custom_fields"]["user_id"])
    db_user.balance += body["data"]["value"]
    db.add(db_user)
    await db.commit()
    return {"message": "Payment received"}

@router.get("/me/items")
async def get_current_user_items(db: DBSession, current_user: CurrentUser, limit: int = 100, offset: int = 0) -> list[ItemRead]:
    statement = select(Item).where(Item.user_id == current_user.id).offset(offset).limit(limit)
    db_items = await db.exec(statement)
    db_items = db_items.all()
    if not db_items:
        raise ItemNotFound()
    return db_items

@router.get("/me/items/{item_id}")
async def get_current_user_item(db: DBSession, current_user: CurrentUser, item_id: int) -> ItemRead:
    statement = select(Item).where(Item.user_id == current_user.id).where(Item.id == item_id)
    db_item = await db.exec(statement)
    db_item = db_item.first()
    if not db_item:
        raise ItemNotFound()
    return db_item

@router.post("/me/items", status_code=201)
async def add_current_user_item(db: DBSession, current_user: CurrentUser, item: ItemCreate) -> ItemRead:
    item.user_id = current_user.id
    db_item = Item(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.patch("/me/items/{item_id}")
async def update_current_user_item(db: DBSession, current_user: CurrentUser, item_id: int, item: ItemUpdate) -> ItemRead:
    statement = select(Item).where(Item.user_id == current_user.id).where(Item.id == item_id)
    db_item = await db.exec(statement)
    db_item = db_item.first()
    if not db_item:
        raise ItemNotFound()
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    await db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.delete("/me/items/{item_id}")
async def delete_current_user_item(db: DBSession, current_user: CurrentUser, item_id: int) -> ItemRead:
    statement = select(Item).where(Item.user_id == current_user.id).where(Item.id == item_id)
    db_item = await db.exec(statement)
    db_item = db_item.first()
    if not db_item:
        raise ItemNotFound()
    await db.delete(db_item)
    await db.commit()
    return db_item

@router.get("/me")
async def get_current_user(current_user: CurrentUser) -> UserRead:
    return current_user

@router.patch("/me")
async def update_current_user(db: DBSession, current_user: CurrentUser, user: UserUpdate) -> UserRead:
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.delete("/me")
async def delete_current_user(db: DBSession, current_user: CurrentUser) -> UserRead:
    current_user.is_active = False
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.get("/")
async def get_users(db: DBSession, limit: int = 100, offset: int = 0) -> list[UserRead]:
    statement = select(User).offset(offset).limit(limit)
    db_users = await db.exec(statement)
    db_users = db_users.all()
    if not db_users:
        raise UserNotFound()
    return db_users

@router.get("/{user_id}")
async def get_user(db: DBSession, user_id: int):
    db_user = await db.get(User, user_id)
    if not db_user:
        raise UserNotFound()
    return db_user

@router.post("/", status_code=201, dependencies=[Depends(require_superuser)])
async def add_user(db: DBSession, user: UserCreate) -> UserRead:
    try:
        user.password = pwd_context.hash(user.password)
        db_user = User(**user.model_dump())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    except IntegrityError:
        raise UserAlreadyExists()
    return db_user

@router.patch("/{user_id}", dependencies=[Depends(require_superuser)])
async def update_user(db: DBSession, user_id: int, user: UserUpdate) -> UserRead:
    db_user = await db.get(User, user_id)
    if not db_user:
        raise UserNotFound()
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", dependencies=[Depends(require_superuser)])
async def delete_user(db: DBSession, user_id: int) -> UserRead:
    db_user = await db.get(User, user_id)
    if not db_user:
        raise UserNotFound()
    db.delete(db_user)
    await db.commit()
    return db_user