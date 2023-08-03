from typing import BinaryIO
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.auth import VerifyToken
from app.models.queries import get_all, get_one, delete, insert_img
from app.models.models import CarouselImage

import cloudinary
import cloudinary.uploader

config = cloudinary.config(secure=True)

router = APIRouter(tags=["carousel"])
token_auth_scheme = HTTPBearer()
table = "CarouselImages"


@router.get("/", response_model=dict[str, CarouselImage])
async def images() -> dict[str, CarouselImage]:
    events = [CarouselImage(**row) for row in get_all(table)]
    return {i.id: i for i in events}


@router.get("/{img_id}", response_model=CarouselImage)
async def image(img_id: str) -> CarouselImage:
    data = get_one(table, img_id)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No carousel image with that id was found",
        )
    return CarouselImage(**data)


@router.delete("/{img_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def del_image(
    img_id: str, token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)
):
    result = VerifyToken(token.credentials).verify()

    if result.get("status"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("msg")
        )

    data = get_one(table, img_id)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="image not found"
        )

    try:
        delete(table, img_id)
        cloudinary.uploader.destroy(img_id)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        )


@router.post("/", response_model=CarouselImage, status_code=status.HTTP_201_CREATED)
async def add_image(
    file: UploadFile, token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)
):
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("msg")
        )

    file_obj: BinaryIO = file.file

    # TODO: reject unsupported filetypes

    img_res: dict = cloudinary.uploader.upload(file_obj)
    img_id = img_res.get("public_id")
    url = img_res.get("url")

    try:
        img = CarouselImage(id=img_id, url=url)  # type: ignore
        insert_img(img)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    return img
