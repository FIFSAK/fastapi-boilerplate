from typing import Any
from datetime import datetime
from fastapi import Depends, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service

from . import router


class Comment(AppModel):
    id: Any = Field(alias="_id")
    content: str
    created_at: datetime
    author_id: str


class GetCommentResponse(AppModel):
    comments: list[Comment]


@router.get("/{shanyrak_id:str}/comments", response_model=GetCommentResponse)
def get_comment(
    shanyrak_id: str,
    svc: Service = Depends(get_service),
) -> GetCommentResponse:
    shanyrak = svc.repository.get_comment(shanyrak_id)
    if shanyrak is None or "comments" not in shanyrak:
        raise HTTPException(
            status_code=404, detail="Shanyrak not found or no comments available"
        )
    return GetCommentResponse(
    comments=[
        Comment(
            _id=str(comment["_id"]),
            content=str(comment["content"]),
            created_at=comment["created_at"],
            author_id=str(comment["author_id"])
        ) for comment in shanyrak["comments"]]
)

