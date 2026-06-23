from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    product_id = Column(Integer, nullable=True)

    user_message = Column(Text)

    ai_response = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )