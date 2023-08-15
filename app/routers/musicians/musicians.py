from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.auth import VerifyToken
from app.models.queries import (
    get_all,
    get_one,
    update_musician,
    get_headshots_by_musician,
)
from app.models.models import Musician, Headshot

router = APIRouter(tags=["musicians"])
token_auth_scheme = HTTPBearer()
table = "Musicians"


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


@router.get("/{musician_id}/headshots", response_model=dict[str, Headshot])
async def headshots(musician_id: int) -> dict[str, Headshot]:
    m = await musician(musician_id)
    return {data["id"]: Headshot(**data) for data in get_headshots_by_musician(m.id)}


@router.put("/{musician_id}", response_model=Musician)
async def update(
    musician_id: int,
    new_m: Musician,
    token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
) -> Musician:
    VerifyToken(token.credentials).verify()

    headshot_data = await headshots(new_m.id)

    if new_m.headshot_id not in headshot_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That headshot isn't in the database",
        )

    m = await musician(musician_id=musician_id)
    try:
        m.bio = new_m.bio
        m.headshot_id = new_m.headshot_id
        update_musician(m)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return m
