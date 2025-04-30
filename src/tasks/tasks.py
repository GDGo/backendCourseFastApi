import asyncio
import os
from PIL import Image

from src.Exceptions import ObjectNotFoundException
from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def compress_and_save_image(input_image_path: str) -> None:
    if not os.path.exists(input_image_path):
        raise ObjectNotFoundException(f"Файл {input_image_path} не найден!")
    output_folder: str = "/app/src/static/images"

    # Открываем изображение
    with Image.open(input_image_path) as img:
        # Получаем имя файла без расширения
        filename = os.path.splitext(os.path.basename(input_image_path))[0]
        ext = os.path.splitext(input_image_path)[1].lower()  # Сохраняем оригинальное расширение

        # Размеры, до которых нужно сжать
        target_widths = [i for i in range(200, 900, 300)]

        for width in target_widths:
            # Вычисляем новую высоту, сохраняя пропорции
            w_percent = width / float(img.size[0])
            height = int(float(img.size[1]) * float(w_percent))

            # Масштабируем изображение
            resized_img = img.resize((width, height), Image.LANCZOS)

            # Формируем имя выходного файла (например, "image_1000.jpg")
            output_filename = f"{filename}_{width}px{ext}"
            output_path = os.path.join(output_folder, output_filename)

            # Сохраняем сжатое изображение
            resized_img.save(output_path, optimize=True, quality=85)
            print(f"Изображение сохранено: {output_path}")


async def get_booking_with_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_chekin()
        print(bookings)


@celery_instance.task(name="booking_today_checkin")
def send_email_to_users_with_today_checkin():
    asyncio.run(get_booking_with_today_checkin_helper())