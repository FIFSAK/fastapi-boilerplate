from fastapi import Depends, HTTPException
from pydantic import BaseModel, Field

from ..service import Service, get_service

from . import router


class Media(BaseModel):
    url: str


class ShanyrakMedia(BaseModel):
    _id: str
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: str
    media: list[Media]


@router.get("/{shanyrak_id:str}/media", response_model=ShanyrakMedia)
def get_shanyrak_media(
    shanyrak_id: str,
    svc: Service = Depends(get_service),
):
    shanyrak = svc.repository.get_shanyrak_media(shanyrak_id)
    if shanyrak is None:
        raise HTTPException(status_code=404, detail="Shanyrak not found")
    return ShanyrakMedia(**shanyrak)
