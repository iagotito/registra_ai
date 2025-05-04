import uuid

from sqlalchemy import Column, String

from app.database.models import Base, BaseModelMixin


class User(BaseModelMixin, Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    def __init__(self, name: str | None, email: str, hashed_password: str):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
