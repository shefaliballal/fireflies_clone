"""ORM model for a recorded meeting and its derived metadata."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.action_item import ActionItem
    from app.models.participant import Participant
    from app.models.transcript import Transcript


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    meeting_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    key_topics: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    participants: Mapped[list["Participant"]] = relationship(
        back_populates="meeting",
    )
    transcripts: Mapped[list["Transcript"]] = relationship(
        back_populates="meeting",
    )
    action_items: Mapped[list["ActionItem"]] = relationship(
        back_populates="meeting",
    )
