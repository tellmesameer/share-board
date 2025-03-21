from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[str]
    text: Mapped[str]


class CodeRequest(BaseModel):
    code: str