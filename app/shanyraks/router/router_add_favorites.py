from typing import Any

from fastapi import Depends, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service

from . import router


    
@router.post("/auth/users/favorites/shanyraks/{shanyrak_id:str}")
def add_favorites(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    data = svc.repository.get_shanyrak(shanyrak_id)
    svc.repository.add_favorites(data)
    return Response(status_code=200)