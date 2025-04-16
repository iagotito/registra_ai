import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

from app.users.services import get_user

from .schemas import HistoryResponse, RecordCreate, RecordResponse

load_dotenv()

POSTGREST_URL = os.environ.get("POSTGREST_URL")


async def register_gain(
    user_id: str, amount: float, description: str
) -> RecordResponse:
    await get_user(user_id)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    record_data = RecordCreate(amount=amount, description=description)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{POSTGREST_URL}/records",
            json={"user_id": user_id, **record_data.model_dump()},
        )
        response.raise_for_status()
        return RecordResponse(**response.json())


async def register_expense(
    user_id: str, amount: float, description: str
) -> RecordResponse:
    await get_user(user_id)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    record_data = RecordCreate(amount=-amount, description=description)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{POSTGREST_URL}/records",
            json={"user_id": user_id, **record_data.model_dump()},
        )
        response.raise_for_status()
        return RecordResponse(**response.json())


async def get_history(user_id: str) -> HistoryResponse:
    await get_user(user_id)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{POSTGREST_URL}/records?user_id=eq.{user_id}&order=created_at.desc"
        )
        response.raise_for_status()
        records = [RecordResponse(**record) for record in response.json()]
        balance = sum(record.amount for record in records)
        return HistoryResponse(history=records, balance=round(balance, 2))
