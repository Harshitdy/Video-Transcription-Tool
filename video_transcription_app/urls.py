from django.urls import path
from .views import transcribe_video

urlpatterns = [
    path('', transcribe_video, name='transcribe_video'),
]
