from django.urls import path
from .views import TranscribeVideoView

urlpatterns = [ 
    # returning the template when user visits the home page "/"
    path('', TranscribeVideoView.as_view(), name='transcribe_video'),
]
