from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

# from .services import get_history, register_expense, register_gain
from app.records.services import get_history, register_expense, register_gain
from app.users.controller import get_current_user
from app.users.schemas import UserResponse

from .schemas import HistoryResponse, RecordCreate, RecordResponse

router = APIRouter(prefix="/api/records", tags=["records"])


@router.post("/gain", response_model=RecordResponse)
async def create_gain(
    record: RecordCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    return await register_gain(current_user.id, record.amount, record.description)


@router.post("/expense", response_model=RecordResponse)
async def create_expense(
    record: RecordCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    return await register_expense(current_user.id, record.amount, record.description)


@router.get("/history", response_model=HistoryResponse)
async def get_history_info(
    current_user: UserResponse = Depends(get_current_user),
):
    return await get_history(current_user.id)
