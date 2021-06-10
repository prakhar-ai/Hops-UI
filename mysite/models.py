from django.db import models

class OngoingJobs(models.Model):
   studyid = models.CharField(max_length=1000)