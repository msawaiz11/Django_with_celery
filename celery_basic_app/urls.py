from django.urls import path, include
# from . import views
from celery_basic_app import views

urlpatterns = [
    path('', views.index, name='index')
]