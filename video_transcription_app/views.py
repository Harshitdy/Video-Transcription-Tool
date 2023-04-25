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
        """
        This function renders a template with a form that allows users to enter a video URL.
        This will return a template when user visits the home page.
        """
        return render(request, 'transcribe_video.html')

    def post(self, request):
        """
        This function downloads a video from a given URL, converts it to audio, transcribes the audio
        using Google speech recognition, saves the video information and transcript to a database, and
        renders a template with the transcription result.
        
        :param request: The HTTP request object that contains information about the current request,
        such as the HTTP method, headers, and data
        :return: a rendered template with the transcription result, which includes the transcript as a
        context variable.
        """
        video_url = request.POST.get('video_url')
        if not video_url:
            messages.error(request, 'Please enter a video URL.')
            return redirect('transcribe_video')

        # Extracts the name of the video from its URL and generates the name for the audio file
        video_name = os.path.basename(video_url)
        audio_name = video_name.split('.')[0] + '.wav'

        # Download video from URL
        try:
            # Uses the requests module to download the video from the provided URL
            video_response = requests.get(video_url, stream=True)

            # Saves the video to the media folder defined in Django's settings
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
            # Uses the ffmpeg tool to convert the video file to an audio file
            audio_path = os.path.join(settings.MEDIA_ROOT, audio_name)
            os.system(f'ffmpeg -i {video_path} -vn -ar 44100 -ac 2 -b:a 192k {audio_path}')
        except Exception as e:
            messages.error(request, f'Failed to convert video to audio: {str(e)}')
            return redirect('transcribe_video')

        # Transcribe audio
        try:
            # Uses the speech_recognition module to transcribe the audio file
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
        # Creates a new Video object and saves it to the database
        video = Video(video_url=video_url, transcript=transcript)
        video.save()

        # Render template with transcription result
        # Renders the transcription result template with the transcript as a context variable
        return render(request, 'transcription_result.html', {'transcript': transcript})


