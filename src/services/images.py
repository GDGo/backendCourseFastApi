import shutil
import time

from fastapi import UploadFile

from src.services.base import BaseService
from src.tasks.tasks import compress_and_save_image


class ImageService(BaseService):
    def upload_file(self, file: UploadFile):
        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)
        time.sleep(10)
        compress_and_save_image.delay(image_path)