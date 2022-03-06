from django.urls import path
from .views import file_upload_view

urlpatterns = [
    path('upload/', file_upload_view)
]
