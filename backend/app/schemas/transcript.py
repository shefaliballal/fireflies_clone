"""Pydantic schemas for the Transcript resource."""

from pydantic import BaseModel, ConfigDict


class TranscriptResponse(BaseModel):
    """Transcript entry data returned from the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_id: int
    speaker: str
    timestamp: int
    text: str
