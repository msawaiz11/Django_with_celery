from django.shortcuts import render
from celery.result import AsyncResult

def index(request):
    return render(request, "image_formats_conversion/index.html")
