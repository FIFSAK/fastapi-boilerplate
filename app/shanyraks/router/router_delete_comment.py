from typing import Any

from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router

@router.delete("/{shanyrak_id:str}/comments/{comment_id:str}")
def delete_comment(
    shanyrak_id: str,
    comment_id: str,
    svc: Service = Depends(get_service),
) -> Response:
    svc.repository.delete_comment(shanyrak_id, comment_id)
    return Response(status_code=200)
