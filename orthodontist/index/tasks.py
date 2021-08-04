from celery import shared_task
from PIL import Image


@shared_task
def image_resizing(path):
    img = Image.open(path)
    img_width, img_height = img.size
    img = img.crop(((img_width - min(img.size)) // 2,
                    (img_height - min(img.size)) // 2,
                    (img_width + min(img.size)) // 2,
                    (img_height + min(img.size)) // 2))
    if img.height > 500 or img.width > 500:
        output_size = (500, 500)
        img.thumbnail(output_size)
    img.save(path)
    return True
