"""CRUD operations for the Meeting model."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.action_item import ActionItem
from app.models.meeting import Meeting
from app.models.participant import Participant
from app.models.transcript import Transcript
from app.schemas.meeting import MeetingCreate, MeetingUpdate
from app.utils.transcript_text import (
    distribute_transcript_timestamps,
    extract_action_items,
    extract_key_topics,
    extract_summary,
    parse_transcript_lines,
)


def get_all_meetings(db: Session) -> list[Meeting]:
    """Return all meetings ordered by newest `created_at` first."""
    stmt = select(Meeting).order_by(Meeting.created_at.desc())
    return list(db.scalars(stmt).all())


def get_meeting_by_id(db: Session, meeting_id: int) -> Meeting | None:
    """Return a single meeting by primary key, or None if not found."""
    return db.get(Meeting, meeting_id)


def get_meeting_with_details(db: Session, meeting_id: int) -> Meeting | None:
    """Return a meeting with related records loaded in a single query."""
    stmt = (
        select(Meeting)
        .options(
            selectinload(Meeting.participants),
            selectinload(Meeting.transcripts),
            selectinload(Meeting.action_items),
        )
        .where(Meeting.id == meeting_id)
    )

    meeting = db.scalars(stmt).first()

    if meeting is None:
        return None

    meeting.transcripts.sort(key=lambda entry: entry.timestamp)

    return meeting


def create_meeting(db: Session, meeting_in: MeetingCreate) -> Meeting:
    """Persist a new meeting and return the created row."""
    meeting = Meeting(**meeting_in.model_dump())

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return meeting


def create_meeting_from_transcript(
    db: Session,
    title: str,
    content: str,
) -> Meeting:
    """
    Create a meeting from an uploaded transcript.

    The upload automatically:
    - estimates meeting duration
    - extracts summary
    - extracts key topics
    - creates transcript entries
    - creates participant records
    """

    entries = parse_transcript_lines(content)

    if not entries:
        raise ValueError("Transcript file contains no readable lines.")

    full_text = " ".join(text for _, text in entries)

    # Estimate duration from transcript length (~130 spoken words/minute)
    word_count = len(full_text.split())
    duration = max(5, min(120, round(word_count / 130)))

    timestamps = distribute_transcript_timestamps(
        duration,
        len(entries),
    )

    unique_speakers = sorted(
        {
            speaker
            for speaker, _ in entries
            if speaker != "Unknown"
        }
    )

    speaker_set = set(unique_speakers)
    action_entries = extract_action_items(entries)

    meeting = Meeting(
        title=title,
        meeting_date=datetime.utcnow(),
        duration=duration,
        summary=extract_summary(full_text, participant_names=speaker_set),
        key_topics=extract_key_topics(full_text, participant_names=speaker_set),

        participants=[
            Participant(
                name=name,
                email=f"{name.lower().replace(' ', '.')}@example.com",
            )
            for name in unique_speakers
        ],

        transcripts=[
            Transcript(
                speaker=speaker,
                timestamp=timestamp,
                text=text,
            )
            for (speaker, text), timestamp in zip(
                entries,
                timestamps,
                strict=True,
            )
        ],

        action_items=[
            ActionItem(task=task, assigned_to=assigned)
            for task, assigned in action_entries
        ],
    )

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return meeting


def update_meeting(
    db: Session,
    meeting: Meeting,
    meeting_in: MeetingUpdate,
) -> Meeting:
    """Apply partial updates to an existing meeting and return the updated row."""

    update_data = meeting_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(meeting, field, value)

    db.commit()
    db.refresh(meeting)

    return meeting


def delete_meeting(db: Session, meeting: Meeting) -> None:
    """Remove a meeting from the database."""
    db.delete(meeting)
    db.commit()