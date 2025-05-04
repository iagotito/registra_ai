from typing import Any, Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import joinedload
from sqlmodel import SQLModel, and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .exceptions import RecordNotFound

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):  # pragma: no cover
    def __init__(self: "BaseRepository", model: Type[ModelType]) -> None:
        self.model = model

    async def add(
        self: "BaseRepository", item: ModelType, db: AsyncSession
    ) -> ModelType:
        db.add(item)
        await db.commit()
        await db.refresh(item)

        return item

    async def get(
        self: "BaseRepository",
        id: int,
        db: AsyncSession,
        eager_join_fields: Optional[list[str]] = None,
    ) -> ModelType:
        stmt = select(self.model).where(
            and_(self.model.id == id, self.model.deleted.is_(False))
        )

        if eager_join_fields is not None and eager_join_fields:
            # Eager loaded Joins
            stmt = stmt.options(
                *[joinedload(getattr(self.model, field)) for field in eager_join_fields]
            )

        result = await db.scalars(stmt)

        record = result.unique().first()

        if not record:
            raise RecordNotFound(f"Item not found with id: {id}")

        return record  # noqa

    async def list(
        self: "BaseRepository",
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
        filters: dict[str, Any] | None = None,
        eager_join_fields: Optional[list[str]] = None,
    ) -> List[ModelType]:
        query = select(self.model).where(self.model.deleted == False).offset(skip).limit(limit)  # type: ignore

        if eager_join_fields is not None and eager_join_fields:
            query = query.options(
                *[joinedload(getattr(self.model, field)) for field in eager_join_fields]
            )

        if filters:
            # Exclude 'skip' and 'limit' from the filters
            model_filters = {
                attr: value
                for attr, value in filters.items()
                if attr not in ["skip", "limit"]
            }

            for attr, value in model_filters.items():
                query = query.where(getattr(self.model, attr) == value)

        result = await db.execute(query)
        return result.scalars().unique().all()

    async def update(
        self: "BaseRepository",
        model: ModelType,
        item: Type[ModelType],
        db: AsyncSession,
    ) -> ModelType:
        obj_data = model.model_dump()
        update_data = item.model_dump(
            exclude_unset=True, exclude={"updated_at", "created_at"}
        )  # type:ignore
        for field in obj_data:
            if field in update_data:
                setattr(model, field, update_data[field])
        db.add(model)
        await db.commit()
        await db.refresh(model)
        return model

    async def delete(self: "BaseRepository", id: int, db: AsyncSession) -> None:
        record = await self.get(id, db)  # type:ignore

        record.deleted = True

        db.add(record)
        await db.commit()
        await db.refresh(record)
