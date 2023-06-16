from fastapi import Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List
from typing import Any
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from . import router


class ShanyrakPreview(BaseModel):
    id: Any = Field(alias="_id")
    address: str


class UserFavorites(BaseModel):
    shanyraks: List[ShanyrakPreview]


@router.get("/auth/users/favorites/shanyraks", response_model=UserFavorites)
def get_user_favorites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> UserFavorites:
    user_id = jwt_data.user_id
    shanyrak_previews = svc.repository.get_user_favorites(user_id)
    if not shanyrak_previews:
        raise HTTPException(status_code=404, detail="No favorites found for this user")
    return UserFavorites(shanyraks=shanyrak_previews)
