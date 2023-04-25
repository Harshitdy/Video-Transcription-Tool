from django.urls import path
from .views import TranscribeVideoView

urlpatterns = [
    path('', TranscribeVideoView.as_view(), name='transcribe_video'),
]
