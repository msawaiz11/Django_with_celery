from django.shortcuts import render
from celery.result import AsyncResult

def index(request):
    return render(request, "celery_basic_app/index.html")
