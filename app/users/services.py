import httpx
from fastapi import HTTPException

from .repositories import UserRepository
from .schemas import UserHashed, UserResponse

user_repository = UserRepository()


async def get_user(user_id: str, token: str) -> UserResponse:
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{POSTGREST_URL}/users?id=eq.{user_id}", headers=headers
        )
        if response.status_code == 404 or not response.json():
            raise HTTPException(status_code=404, detail=f"User id not found: {user_id}")
        return UserResponse(**response.json()[0])


async def get_or_create_user(
    google_id: str, name: str, email: str, picture: str, token: str
) -> UserResponse:
    try:
        return await get_user(google_id, token)
    except HTTPException as e:
        if e.status_code != 404:
            raise
        user_data = UserHashed(
            id=google_id, name=name, email=email, profile_pic=picture
        )
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{POSTGREST_URL}/users", json=user_data.model_dump(), headers=headers
            )
            response.raise_for_status()
            return UserResponse(**response.json())
