from django.db import models

# Create your models here.
class Video(models.Model):
    video_url = models.URLField()
    transcript = models.TextField(blank=True, null=True)


    



# username = valartech
# password = Valar
# video_url = https://www.taxmann.com/emailer/images/CompaniesAct.mp4