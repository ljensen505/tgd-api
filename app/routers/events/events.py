from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.auth import VerifyToken
from app.models.queries import delete, get_all, get_one, insert_event
from app.models.models import Event
from datetime import datetime

router = APIRouter(tags=["events"])
token_auth_scheme = HTTPBearer()
table = "Events"


@router.get("/", response_model=dict[int, Event])
async def events() -> dict[int, Event]:
    events = [Event(**row) for row in get_all(table)]
    return {e.id: e for e in events if e.id}


@router.get("/{event_id}", response_model=Event)
async def event(event_id: int) -> Event:
    data = get_one(table, event_id)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No event with that id was found",
        )

    return Event(**data)


@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def add_event(
    event: Event, token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)
) -> Event:
    VerifyToken(token.credentials).verify()

    try:
        insert_event(event)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    return event


@router.delete(
    "/{event_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def del_event(
    event_id: int, token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)
) -> None:
    VerifyToken(token.credentials).verify()
    e = await event(event_id=event_id)
    if e.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error reading that event id from database",
        )
    try:
        delete(table=table, id=e.id)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


# optional TODO add put method, but simply allowing posting and deleting is probably fine
