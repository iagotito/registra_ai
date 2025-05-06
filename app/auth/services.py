from typing import Dict

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.jwt import create_access_token
from app.database.database import get_database
from app.users.models import User
from app.users.repositories import UsersRepository
from app.users.schemas import UserCreate, UserHashed, UserLogin, UserResponse

# Configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_user(user: UserCreate) -> dict:
    async with get_database() as db:
        user_repo = UsersRepository()
        existing_user = await user_repo.list(
            db=db, filters={"email": user.email.lower()}
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )

        try:
            new_user = User(
                name=user.name,
                email=user.email.lower(),
                hashed_password=hash_password(user.password),
            )
            created_user = await user_repo.add(new_user, db)
            access_token = create_access_token(
                data={"sub": str(created_user.id), "email": created_user.email}
            )
            return {
                "user_data": UserResponse.model_validate(created_user),
                "access_token": access_token,
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user",
            )


async def authenticate_user(user: UserLogin) -> Dict[str, str]:
    async with get_database() as db:
        user_repo = UsersRepository()
        try:
            users = await user_repo.list(db=db, filters={"email": user.email.lower()})
            if not users:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials: email not found",
                )

            db_user = users[0]
            if not verify_password(user.password, str(db_user.hashed_password)):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials: invalid password",
                )
            if bool(db_user.deleted):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive"
                )

            access_token = create_access_token(
                data={"sub": str(db_user.id), "email": db_user.email}
            )
            return {"access_token": access_token, "token_type": "bearer"}

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
