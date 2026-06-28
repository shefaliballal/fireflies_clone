"""
Aggregate API router that mounts all domain-specific routers.

Adding a new feature area (e.g. meetings) means creating a router module under
`app/api/` and including it here with a path prefix.
"""

from fastapi import APIRouter

from app.api import action_items, health, meetings

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(meetings.router)
api_router.include_router(action_items.router)
