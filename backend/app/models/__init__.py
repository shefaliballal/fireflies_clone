"""
SQLAlchemy ORM models for the Fireflies clone backend.

Import every model here so `Base.metadata` registers all tables before
`init_db()` runs.
"""

from app.models.action_item import ActionItem
from app.models.meeting import Meeting
from app.models.participant import Participant
from app.models.transcript import Transcript

__all__ = [
    "ActionItem",
    "Meeting",
    "Participant",
    "Transcript",
]
