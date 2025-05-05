from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.repositories import BaseRepository
from app.users.models import User
from app.users.schemas import UserHashed


class UsersRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def add(self: "UsersRepository", item: UserHashed, db: AsyncSession):
        return await super().add(item, db)  # type: ignore
