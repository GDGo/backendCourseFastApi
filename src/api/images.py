import shutil
from fastapi import APIRouter, UploadFile

from src.tasks.tasks import compress_and_save_image


router = APIRouter(
    prefix="/images",
    tags=["Изображения"]
)


@router.post("")
def upload_file(file: UploadFile):
    image_path = f"src\static\images\\{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    compress_and_save_image.delay(image_path)