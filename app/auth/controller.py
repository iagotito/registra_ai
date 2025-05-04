from fastapi import APIRouter, status

from app.auth.services import authenticate_user, create_user
from app.users.schemas import UserCreate, UserHashed, UserLogin, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(user: UserCreate):
    return await create_user(user)


@router.post("/login")
async def login_user(user: UserLogin):
    return await authenticate_user(user)
