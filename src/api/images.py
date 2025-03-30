import shutil
from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends

from src.api.dependencies import UserIdDep
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
    image_path = f"src\static\images\\{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    compress_and_save_image.delay(image_path)