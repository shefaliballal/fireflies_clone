"""REST endpoints for action item resources."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import action_item as action_item_crud
from app.database import get_db
from app.schemas.action_item import ActionItemResponse, ActionItemUpdate

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.patch(
    "/{action_item_id}",
    response_model=ActionItemResponse,
    summary="Update action item",
)
def update_action_item(
    action_item_id: int,
    action_item_in: ActionItemUpdate,
    db: Session = Depends(get_db),
) -> ActionItemResponse:
    """Update an action item's completion status."""
    action_item = action_item_crud.get_action_item_by_id(db, action_item_id)
    if action_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action item {action_item_id} not found",
        )
    return action_item_crud.update_action_item(db, action_item, action_item_in)
