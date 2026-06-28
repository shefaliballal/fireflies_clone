"""REST endpoints for meeting resources."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.crud import meeting as meeting_crud
from app.database import get_db
from app.schemas.meeting import (
    MeetingCreate,
    MeetingDetailResponse,
    MeetingResponse,
    MeetingUpdate,
)
from app.utils.transcript_text import title_from_filename

router = APIRouter(prefix="/meetings", tags=["meetings"])

ALLOWED_EXTENSIONS = (".txt", ".md")


@router.get("", response_model=list[MeetingResponse], summary="List meetings")
def list_meetings(db: Session = Depends(get_db)) -> list[MeetingResponse]:
    """Return all meetings, newest first."""
    return meeting_crud.get_all_meetings(db)


@router.post(
    "/upload",
    response_model=MeetingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload transcript file",
)
async def upload_meeting_transcript(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> MeetingResponse:
    """Create a meeting from a plain-text transcript upload."""
    filename = file.filename or ""
    if not any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .txt and .md files are supported.",
        )

    raw_content = await file.read()
    try:
        content = raw_content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transcript file must be valid UTF-8 text.",
        ) from exc

    title = title_from_filename(filename)

    try:
        return meeting_crud.create_meeting_from_transcript(db, title, content)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/{meeting_id}",
    response_model=MeetingDetailResponse,
    summary="Get meeting by ID",
)
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
) -> MeetingDetailResponse:
    """Return a single meeting with participants, transcript, and action items."""
    meeting = meeting_crud.get_meeting_with_details(db, meeting_id)
    if meeting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meeting {meeting_id} not found",
        )
    return meeting


@router.post(
    "",
    response_model=MeetingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create meeting",
)
def create_meeting(
    meeting_in: MeetingCreate,
    db: Session = Depends(get_db),
) -> MeetingResponse:
    """Create a new meeting record."""
    return meeting_crud.create_meeting(db, meeting_in)


@router.put(
    "/{meeting_id}",
    response_model=MeetingResponse,
    summary="Update meeting",
)
def update_meeting(
    meeting_id: int,
    meeting_in: MeetingUpdate,
    db: Session = Depends(get_db),
) -> MeetingResponse:
    """Update an existing meeting. Only provided fields are changed."""
    meeting = meeting_crud.get_meeting_by_id(db, meeting_id)
    if meeting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meeting {meeting_id} not found",
        )
    return meeting_crud.update_meeting(db, meeting, meeting_in)


@router.delete(
    "/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete meeting",
)
def delete_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a meeting by its primary key."""
    meeting = meeting_crud.get_meeting_by_id(db, meeting_id)
    if meeting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meeting {meeting_id} not found",
        )
    meeting_crud.delete_meeting(db, meeting)
