from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.auth import VerifyToken
from app.models.queries import get_all, get_one, update_musician
from app.models.models import Musician

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


@router.put("/", response_model=Musician)
async def update(
    new_m: Musician,
    token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
) -> Musician:
    VerifyToken(token.credentials).verify()

    # TODO: add headshot router AND verify that newly associated headshot exists

    m = await musician(new_m.id)
    try:
        m.bio = new_m.bio
        m.headshot = new_m.headshot
        update_musician(m)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return m
