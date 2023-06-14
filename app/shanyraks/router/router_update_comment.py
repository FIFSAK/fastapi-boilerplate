from typing import Any

from fastapi import Depends, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from ..service import Service, get_service

from . import router


class UpdateCommentRequest(AppModel):
    content: str


@router.patch("/{shanyrak_id:str}/comments/{comment_id:str}")
def update_comment(
    shanyrak_id: str,
    comment_id: str,
    input: UpdateCommentRequest,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    svc.repository.update_comment(shanyrak_id, comment_id, input.content)
    return Response(status_code=200)
