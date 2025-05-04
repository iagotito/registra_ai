import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .schemas import UserResponse
from .services import get_user

router = APIRouter(prefix="/users", tags=["users"])
load_dotenv()

# async def get_current_user(
