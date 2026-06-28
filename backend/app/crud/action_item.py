"""CRUD operations for the ActionItem model."""

from sqlalchemy.orm import Session

from app.models.action_item import ActionItem
from app.schemas.action_item import ActionItemUpdate


def get_action_item_by_id(db: Session, action_item_id: int) -> ActionItem | None:
    """Return a single action item by primary key, or None if not found."""
    return db.get(ActionItem, action_item_id)


def update_action_item(
    db: Session,
    action_item: ActionItem,
    action_item_in: ActionItemUpdate,
) -> ActionItem:
    """Apply updates to an action item and return the updated row."""
    action_item.completed = action_item_in.completed
    db.commit()
    db.refresh(action_item)
    return action_item
