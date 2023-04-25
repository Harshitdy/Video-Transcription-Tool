import os
import requests
import speech_recognition as sr
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .models import Video

class TranscribeVideoView(View):
    def get(self, request):
        return render(request, 'transcribe_video.html')

    def post(self, request):
        video_url = request.POST.get('video_url')
        if not video_url:
            messages.error(request, 'Please enter a video URL.')
            return redirect('transcribe_video')

        video_name = os.path.basename(video_url)
        audio_name = video_name.split('.')[0] + '.wav'

        # Download video from URL
        try:
            video_response = requests.get(video_url, stream=True)
            video_path = os.path.join(settings.MEDIA_ROOT, video_name)
            with open(video_path, 'wb') as f:
                for chunk in video_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        except Exception as e:
            messages.error(request, f'Failed to download video: {str(e)}')
            return redirect('transcribe_video')

        # Convert video to audio
        try:
            audio_path = os.path.join(settings.MEDIA_ROOT, audio_name)
            os.system(f'ffmpeg -i {video_path} -vn -ar 44100 -ac 2 -b:a 192k {audio_path}')
        except Exception as e:
            messages.error(request, f'Failed to convert video to audio: {str(e)}')
            return redirect('transcribe_video')

        # Transcribe audio
        try:
            r = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = r.record(source)
                transcript = r.recognize_google(audio)
        except sr.RequestError:
            messages.error(request, 'Failed to connect to the Google speech recognition service.')
            return redirect('transcribe_video')
        except sr.SpeechRecognitionError as e:
            messages.error(request, f'Failed to transcribe audio: {str(e)}')
            return redirect('transcribe_video')

        # Save video information and transcript to database
        video = Video(video_url=video_url, transcript=transcript)
        video.save()

        # Render template with transcription result
        return render(request, 'transcription_result.html', {'transcript': transcript})


