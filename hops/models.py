from django.db import models

class Report(models.Model):
    studyid = models.CharField(max_length=50)
    Main_Img = models.ImageField(upload_to='images/')
    
class Save_report(models.Model):
    studyid = models.CharField(max_length=100)
    my_data = models.TextField()