# celery_basic_app/tasks.py
from celery import shared_task
from django.conf import settings
from pdf2docx import Converter

from datetime import datetime
from docx2pdf import convert
import logging

logger = logging.getLogger(__name__)

@shared_task
def docx_to_pdf(input_path, output_path):
    try:
        convert(input_path, output_path)
        return {'output_path': output_path}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@shared_task
def pdf_to_docx(input_path_pdf, output_path_docx):
    logger.info(f"Converting {input_path_pdf} to {output_path_docx}")
    cv = Converter(input_path_pdf)
    cv.convert(output_path_docx)
    cv.close()
    logger.info(f"Successfully converted {input_path_pdf} to {output_path_docx}")
    return output_path_docx