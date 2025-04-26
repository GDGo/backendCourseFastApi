import shutil

from fastapi import APIRouter, UploadFile, Depends

from src.api.dependencies import UserIdDep
from src.services.images import ImageService
from src.tasks.tasks import compress_and_save_image


router = APIRouter(
    prefix="/images",
    tags=["Изображения"]
)


@router.post("")
def upload_file(
        file: UploadFile,
        user_id: UserIdDep
):
    ImageService().upload_file(file=file)
    return {"status": "OK"}