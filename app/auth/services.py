import httpx
from fastapi import HTTPException
from jose import jwt

from app.users.services import get_or_create_user

GOOGLE_CLIENT_ID = "your-client-id"
GOOGLE_CLIENT_SECRET = "your-client-secret"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


async def get_google_provider_cfg():
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_DISCOVERY_URL)
        response.raise_for_status()
        return response.json()


async def google_login(code: str, redirect_uri: str) -> str:
    cfg = await get_google_provider_cfg()
    token_endpoint = cfg["token_endpoint"]
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            token_endpoint,
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        token_response.raise_for_status()
        tokens = token_response.json()
        userinfo_response = await client.get(
            cfg["userinfo_endpoint"],
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        userinfo_response.raise_for_status()
        user_info = userinfo_response.json()
        if not user_info.get("email_verified"):
            raise HTTPException(status_code=400, detail="User email not verified")
        user = await get_or_create_user(
            user_info["sub"],
            user_info["given_name"],
            user_info["email"],
            user_info.get("picture"),
        )
        token = jwt.encode({"sub": user.id}, SECRET_KEY, algorithm=ALGORITHM)
        return token
