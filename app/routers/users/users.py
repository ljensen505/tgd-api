from fastapi import APIRouter, HTTPException, status
from app.models.queries import get_all, get_one
from app.models.models import User

router = APIRouter(tags=["users"])
table = "Users"


@router.get("/", response_model=dict[str, User])
async def users() -> dict[str, User]:
    users = [User(**row) for row in get_all(table)]
    return {u.id: u for u in users}


@router.get("/{user_id}", response_model=User)
async def user(user_id: str) -> User:
    data = get_one(table, user_id)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user with that id was found",
        )
    return User(**data)
