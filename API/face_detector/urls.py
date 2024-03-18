from django.urls import path
from .views import detect_faces

urlpatterns = [
    path('detect/', detect_faces, name='detect_faces'),
]