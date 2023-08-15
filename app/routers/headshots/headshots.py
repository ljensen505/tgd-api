from typing import BinaryIO

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.auth import VerifyToken
from app.models.queries import get_all, get_one, insert_headshot
from app.models.models import Musician, Headshot
from app.routers.carousel.carousel import get_file_extension
from app.routers.musicians.musicians import musician
import cloudinary
import cloudinary.uploader

config = cloudinary.config(secure=True)

router = APIRouter(tags=["headshots"])
token_auth_scheme = HTTPBearer()
table = "Headshots"

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


@router.get("/", response_model=dict[str, Headshot])
async def headshots() -> dict[str, Headshot]:
    headshots_list = [Headshot(**data) for data in get_all(table)]
    return {h.id: h for h in headshots_list}


@router.post(
    "/{musician_id}", response_model=Headshot, status_code=status.HTTP_201_CREATED
)
async def add_image(
    musician_id: int,
    file: UploadFile,
    token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
):
    VerifyToken(token.credentials).verify()

    m = await musician(musician_id)

    file_obj: BinaryIO = file.file
    file_ext = get_file_extension(file.filename)

    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"must be jpg or png, not {file_ext}",
        )

    img_res: dict = cloudinary.uploader.upload(file_obj)
    img_id: str = img_res.get("public_id")  # type: ignore
    url: str = img_res.get("url")  # type: ignore

    try:
        img = Headshot(id=img_id, url=url, musician_id=m.id)
        insert_headshot(img)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    return img


# TODO: add tests for this endpoint
