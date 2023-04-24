import os
import requests
from django.conf import settings
from django.shortcuts import render
import speech_recognition as sr
from .models import Video



def transcribe_video(request):
    if request.method == 'POST':
        video_url = request.POST['video_url']
        video_name = os.path.basename(video_url)
        audio_name = video_name.split('.')[0] + '.wav'

        # Download video from URL
        video_response = requests.get(video_url, stream=True)
        video_path = os.path.join(settings.MEDIA_ROOT, video_name)
        with open(video_path, 'wb') as f:
            for chunk in video_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        # Convert video to audio
        audio_path = os.path.join(settings.MEDIA_ROOT, audio_name)
        os.system(f'ffmpeg -i {video_path} -vn -ar 44100 -ac 2 -b:a 192k {audio_path}')

        # Transcribe audio
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
            transcript = r.recognize_google(audio)

        # Save video information and transcript to database
        video = Video(video_url=video_url, transcript=transcript)
        video.save()

        # Render template with transcription result
        return render(request, 'transcription_result.html', {'transcript': transcript})

    # If request method is not POST, render upload form
    return render(request, 'transcribe_video.html')


