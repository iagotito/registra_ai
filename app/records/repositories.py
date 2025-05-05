from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.repositories import BaseRepository
from app.records.models import Record


class RecordsRepository(BaseRepository[Record]):
    def __init__(self):
        super().__init__(Record)

    # async def add(self: "UsersRepository", item: UserHashed, db: AsyncSession):
    # return await super().add(item, db)  # type: ignore
