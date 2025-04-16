from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from .services import GOOGLE_CLIENT_ID, get_google_provider_cfg, google_login

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def login():
    cfg = await get_google_provider_cfg()
    auth_url = f"{cfg['authorization_endpoint']}?client_id={GOOGLE_CLIENT_ID}&response_type=code&redirect_uri=http://localhost:8000/auth/callback&scope=openid%20email%20profile"
    return RedirectResponse(auth_url)


@router.get("/callback")
async def callback(code: str):
    token = await google_login(code, "http://localhost:8000/auth/callback")
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
async def logout():
    # JWT is stateless; client should discard token
    return {"message": "Logged out"}
