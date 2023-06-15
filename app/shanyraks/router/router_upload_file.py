from fastapi import Depends, UploadFile
from typing import List

from ..service import Service, get_service
from . import router


@router.post("/{shanyrak_id:str}/media")
def upload_files(
    shanyrak_id: str,
    files: List[UploadFile],
    svc: Service = Depends(get_service),
):
    
    result = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        result.append(url)
    svc.repository.add_media(shanyrak_id, result)
    return {"msg": "Files uploaded successfully"}
