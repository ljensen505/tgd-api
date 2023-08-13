from fastapi import APIRouter, HTTPException, status
from app.models.queries import get_all, get_one
from app.models.models import Musician

router = APIRouter(tags=["musicians"])
table = "Musicians"

# TODO: add functionality for:
# edit bio
# replace headshot


@router.get("/", response_model=dict[int, Musician])
async def musicians() -> dict[int, Musician]:
    musicians = [Musician(**row) for row in get_all(table)]
    return {m.id: m for m in musicians}


@router.get("/{musician_id}", response_model=Musician)
async def musician(musician_id: int) -> Musician:
    data = get_one(table, musician_id)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No musician with that id was found",
        )
    return Musician(**data)
