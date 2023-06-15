from typing import Any

from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router


@router.delete("/{shanyrak_id:str}/media")
def delete_media(
    shanyrak_id: str,
    urls: list[str],
    svc: Service = Depends(get_service),
) -> Response:
    svc.repository.delete_media(shanyrak_id, urls)
    return Response(status_code=200)
