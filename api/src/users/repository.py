from sqlmodel import select
from pydantic import EmailStr

from src.repository import BaseRepository
from src.postgres import AsyncSession

from src.users.models import User


class UsersRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_email(self, email: EmailStr):
        statement = select(User).where(User.email == email)
        db_user = await self.db.exec(statement)
        db_user = db_user.first()
        return db_user
