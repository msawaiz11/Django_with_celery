from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('celery_basic/', include('celery_basic_app.urls')),
    path('image_format/', include('image_formats_conversion.urls'))
    
]

