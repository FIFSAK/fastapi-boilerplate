from typing import Any

from fastapi import Depends, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service

from . import router


class AddCommentRequest(AppModel):
    content : str


@router.post("/{shanyrak_id:str}/comments")
def add_comment(
    shanyrak_id: str,
    input: AddCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    author_id =jwt_data.user_id
    svc.repository.add_comment(shanyrak_id, author_id, input.dict())
    return Response(status_code=200)