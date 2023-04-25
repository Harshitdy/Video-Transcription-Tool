# Video-Transcription-Tool
this is a web application using Python, Django, and a speech recognition library that converts a given video or a short URL into a transcript.

 > This is a web application that allows users to transcribe the audio from a video file. The user enters the URL of the video they want to transcribe, and the application uses the requests library to download the video from the URL. It then uses the ffmpeg library to convert the video file to an audio file in WAV format, and the speech_recognition library to transcribe the audio to text.
 
## To run this

### 1. Clone the repository
 ```
 git clone https://github.com/Harshitdy/Video-Transcription-Tool.git
 ```
 
 ### 2. Create a virtual environment.
 ```
 python -m venv .venv
 ```
 
 ### 3. Activate the virtual environment.
 ```
 source .venv/bin/activate
 ```
 
 ### 4. Go to Project Directory
 ```
 cd video_transcription_project
 ```
 
 ### 5. Install the requirements.
 ```
 pip install -r requirements.txt
 ```
 
 ### 6. Run the server by opening the terminal into project directory
 ```
 python manage.py runserver
 ```
 
 ### 7. Go to Your preferred browser and open a new tab and type this.
 
 ```
 http://127.0.0.1:8000
 ```
 
 ###. 8 Enter your Video Url which you want to transcribe.
 
 ![image](/images/Screenshot1.png)
 
 
### 9. Use this url for testing.
```
https://www.taxmann.com/emailer/images/CompaniesAct.mp4
```

# You will get transcription in just few seconds.






