from fastapi import APIRouter, HTTPException, status
from app.models.models import Group
from app.models.queries import get_group, update_group_bio


router = APIRouter(tags=["group"])


@router.get("/", response_model=Group)
async def group() -> Group:
    data = get_group()
    return Group(**data)


@router.put("/", response_model=Group)
async def update_bio(new_group: Group) -> Group:
    if new_group.name != "The Grapefruits Duo":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group name either missing or malformed. You cannot change the group name",
        )

    update_group_bio(new_group.bio)

    g: Group = await group()
    return g
