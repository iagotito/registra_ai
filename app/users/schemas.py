from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    profile_pic: str | None


class UserCreate(UserBase):
    id: str


class UserResponse(UserBase):
    id: str
