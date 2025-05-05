from sqlalchemy import Column, ForeignKey, Integer, String

from app.database.models import Base, BaseModelMixin


class Record(BaseModelMixin, Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String, nullable=False)

    def __init__(self, user_id: str | None, amount: int, description: str):
        self.user_id = user_id
        self.amount = amount
        self.description = description
