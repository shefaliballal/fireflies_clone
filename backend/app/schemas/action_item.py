"""Pydantic schemas for the ActionItem resource."""

from pydantic import BaseModel, ConfigDict


class ActionItemResponse(BaseModel):
    """Action item data returned from the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_id: int
    task: str
    assigned_to: str | None
    completed: bool


class ActionItemUpdate(BaseModel):
    """Fields that can be updated on an action item."""

    completed: bool
