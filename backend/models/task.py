import uuid
from datetime import datetime
from typing import List
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    view_id: Mapped[str] = mapped_column(String, ForeignKey("views.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    view: Mapped["View"] = relationship("View", back_populates="tasks")
    logs: Mapped[List["CompletionLog"]] = relationship("CompletionLog", back_populates="task", cascade="all, delete-orphan")
