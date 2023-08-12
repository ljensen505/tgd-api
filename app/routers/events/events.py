from fastapi import APIRouter, HTTPException, status
from app.models.queries import get_all, get_one
from app.models.models import Event
from datetime import datetime

router = APIRouter(tags=["events"])
table = "Events"


@router.get("/", response_model=dict[int, Event])
async def events() -> dict[int, Event]:
    events = [Event(**row) for row in get_all(table)]
    return {e.id: e for e in events}


@router.get("/{event_id}", response_model=Event)
async def event(event_id: int) -> Event:
    data = get_one(table, event_id)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No event with that id was found",
        )
    return Event(
        id=data["id"],
        name=data["name"],
        date=datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S"),
        location=data["location"],
        description=data["description"],
        image_url=data["image_url"],
        ticket_url=data["ticket_url"],
    )


# TODO: add post and put functionality
