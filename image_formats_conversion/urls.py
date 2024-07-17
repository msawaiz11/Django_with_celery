from django.urls import path, include
from image_formats_conversion import views

urlpatterns = [
    path('', views.index, name='index')
]