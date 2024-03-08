from sqlmodel import select
from pydantic import EmailStr

from src.repository import BaseRepository
from src.postgres import AsyncSession

from src.users.models import User
from src.users.exceptions import UserNotFound


class UsersRepository(BaseRepository[User]):
    def __init__(self, postgres: AsyncSession):
        super().__init__(postgres, User)

    async def get_by_email(self, email: EmailStr):
        statement = select(User).where(User.email == email)
        db_user = await self.postgres.exec(statement)
        db_user = db_user.first()
        if not db_user:
            raise UserNotFound()
        return db_user
