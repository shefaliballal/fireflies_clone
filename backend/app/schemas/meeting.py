"""Pydantic schemas for the Meeting resource."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.action_item import ActionItemResponse
from app.schemas.participant import ParticipantResponse
from app.schemas.transcript import TranscriptResponse


class MeetingCreate(BaseModel):
    """Payload for creating a new meeting."""

    title: str
    meeting_date: datetime
    duration: int
    summary: str | None = None
    key_topics: str | None = None


class MeetingUpdate(BaseModel):
    """Payload for partially updating an existing meeting."""

    title: str | None = None
    meeting_date: datetime | None = None
    duration: int | None = None
    summary: str | None = None
    key_topics: str | None = None


class MeetingResponse(BaseModel):
    """Meeting data returned from the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    meeting_date: datetime
    duration: int
    summary: str | None
    key_topics: str | None
    created_at: datetime


class MeetingDetailResponse(MeetingResponse):
    """Meeting with related participants, transcript, and action items."""

    participants: list[ParticipantResponse] = Field(default_factory=list)
    transcripts: list[TranscriptResponse] = Field(default_factory=list)
    action_items: list[ActionItemResponse] = Field(default_factory=list)
