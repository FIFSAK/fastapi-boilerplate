from fastapi import Depends, UploadFile
from typing import List
from app.auth.adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router


from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


@router.post("/auth/users/avatar")
def upload_avatar(
    file: UploadFile,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    """
    file.filename: str - Название файла
    file.file: BytesIO - Содержимое файла
    """
    url = svc.s3_service.upload_file(file.file, file.filename)
    svc.repository.upload_avatar(jwt_data.user_id, url)
    return {"msg": "Files uploaded successfully"}
