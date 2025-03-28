import os
from time import sleep
from PIL import Image

from src.tasks.celery_app import celery_instance


@celery_instance.task
def compress_and_save_image(input_image_path: str) -> None:
    if not os.path.exists(input_image_path):
        raise FileNotFoundError(f"Файл {input_image_path} не найден!")
    output_folder: str = "src\static\images"

    # Открываем изображение
    with Image.open(input_image_path) as img:
        # Получаем имя файла без расширения
        filename = os.path.splitext(os.path.basename(input_image_path))[0]
        ext = os.path.splitext(input_image_path)[1].lower()  # Сохраняем оригинальное расширение

        # Размеры, до которых нужно сжать
        target_widths = [i for i in range(10000, 100000, 1000)]

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