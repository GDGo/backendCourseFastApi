import shutil

from fastapi import APIRouter, UploadFile, Depends

from src.Exceptions import ObjectNotFoundException, FileNotFoundErrorHTTPException
from src.api.dependencies import UserIdDep
from src.services.images import ImageService
from src.tasks.tasks import compress_and_save_image


router = APIRouter(
    prefix="/images",
    tags=["Изображения"]
)


@router.post("", name="Загрузка фотографии")
def upload_file(
        file: UploadFile,
        user_id: UserIdDep
):
    try:
        ImageService().upload_file(file=file)
        return {"status": "OK"}
    except ObjectNotFoundException:
        raise FileNotFoundErrorHTTPException()