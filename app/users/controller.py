from fastapi import APIRouter, Depends, status

from app.users.services import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user_from_token(user_data: dict = Depends(get_current_user)):
    return user_data
