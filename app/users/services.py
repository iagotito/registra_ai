from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.jwt import verify_token
from app.database.database import get_database
from app.users.schemas import UserResponse

from .repositories import UsersRepository

user_repository = UsersRepository()

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserResponse:
    token = credentials.credentials
    try:
        payload = verify_token(token)
    except HTTPException:
        raise  # already raises 401

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid token payload")

    async with get_database() as db:
        user = await user_repository.get(id=user_id, db=db)
        return UserResponse.model_validate(user)
