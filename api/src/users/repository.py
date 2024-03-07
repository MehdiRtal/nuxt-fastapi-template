from sqlmodel import select
from pydantic import EmailStr

from src.repository import BaseRepository
from src.postgres import AsyncSession

from src.users.models import User


class UsersRepository(BaseRepository[User]):
    def __init__(self, postgres: AsyncSession):
        super().__init__(postgres, User)

    async def get_by_email(self, email: EmailStr):
        statement = select(User).where(User.email == email)
        postgres_user = await self.postgres.exec(statement)
        postgres_user = postgres_user.first()
        return postgres_user
