from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from .schemas import UserResponse
from .services import get_user

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    # Placeholder: Implement JWT decoding later
    user_id = token  # Simplified; replace with actual user_id extraction
    return await get_user(user_id)


@router.get("/me", response_model=UserResponse)
async def get_user_data(current_user: UserResponse = Depends(get_current_user)):
    return current_user
