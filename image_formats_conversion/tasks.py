from celery import shared_task
from django.conf import settings
from PIL import Image


@shared_task
def jpgtopng(input_image_path, output_image_path):
    img = Image.open(input_image_path)
    img.save(output_image_path, 'PNG')
    return output_image_path