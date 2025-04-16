from datetime import datetime

from pydantic import BaseModel


class RecordBase(BaseModel):
    amount: float
    description: str


class RecordCreate(RecordBase):
    pass


class RecordResponse(RecordBase):
    id: int
    user_id: str
    created_at: datetime


class HistoryResponse(BaseModel):
    history: list[RecordResponse]
    balance: float
