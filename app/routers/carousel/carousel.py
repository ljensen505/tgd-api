from fastapi import APIRouter, HTTPException, status
from app.models.queries import get_all, get_one
from app.models.models import CarouselImage

router = APIRouter(tags=["carousel"])
table = "CarouselImages"


@router.get("/", response_model=dict[str, CarouselImage])
async def images() -> dict[str, CarouselImage]:
    events = [CarouselImage(**row) for row in get_all(table)]
    return {i.id: i for i in events}


@router.get("/{img_id}", response_model=CarouselImage)
async def event(img_id: str) -> CarouselImage:
    data = get_one(table, img_id)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No carousel image with that id was found",
        )
    return CarouselImage(**data)
