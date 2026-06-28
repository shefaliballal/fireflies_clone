"""Pydantic schemas for the Participant resource."""

from pydantic import BaseModel, ConfigDict


class ParticipantResponse(BaseModel):
    """Participant data returned from the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_id: int
    name: str
    email: str | None
