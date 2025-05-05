from fastapi import HTTPException

from app.database.database import get_database
from app.records.models import Record
from app.records.repositories import RecordsRepository
from app.records.schemas import HistoryResponse, RecordResponse

records_repository = RecordsRepository()


async def register_gain(
    user_id: str, amount: float, description: str
) -> RecordResponse:
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    int_amount = int(amount * 100)
    async with get_database() as db:
        record_data = Record(
            user_id=user_id, amount=int_amount, description=description
        )
        new_record = await records_repository.add(record_data, db)
        new_record.amount /= 100  # type: ignore
        return RecordResponse.model_validate(new_record)


async def register_expense(
    user_id: str, amount: float, description: str
) -> RecordResponse:
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    amount = amount * -1
    int_amount = int(amount * 100)
    async with get_database() as db:
        record_data = Record(
            user_id=user_id, amount=int_amount, description=description
        )
        new_record = await records_repository.add(record_data, db)
        new_record.amount /= 100  # type: ignore
        return RecordResponse.model_validate(new_record)


async def get_history(user_id: str) -> HistoryResponse:
    async with get_database() as db:
        filters = {"user_id": user_id}
        history_data = await records_repository.list(db=db, filters=filters)
        balance: float = 0
        history = []

        for rec in history_data:
            rec.amount /= 100  # type: ignore
            history.append(rec)
            balance += rec.amount  # type: ignore

        return HistoryResponse(history=history, balance=balance)
