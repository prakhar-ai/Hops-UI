from django.shortcuts import render
import requests
import json
from django.http import HttpResponse
from hops.models import OngoingJobs
from django.http import JsonResponse
# Create your views here.

def home_page(request):
    return render(request,'base.html')

def prediction(request):
    return render(request,'prediction.html')

def report(request):
    return render(request,'report.html')

def faqs(request):
    return render(request,'faqs.html')

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def files(request):
    return render(request,'files.html')

def comments(request):
    return render(request,'comments.html')

def vtkviewer(request):
    return render(request,'vtkviewer.html')

def jobs(request):
    return render(request,'jobs.html')

def getreport(request):
    id = request.POST.get("studyid")
    post_data = {'study_instance_ids': str(id)}
    jobs = OngoingJobs(studyid=id)
    jobs.save()
    requests.post('http://192.168.1.196:5000/analyze', data=post_data)

def studyid(request):
    study_ids = OngoingJobs.objects.all().values_list('studyid', flat=True) 
    study_ids = list(set(study_ids)) 
    id = ','.join(study_ids)
    post_data = {'study_instance_ids': str(id)}
    percent_completed = requests.post('http://192.168.1.196:5000/get_progress_percents', data=post_data)
    status = []
    for i in percent_completed:
        if i=='100':
            status.append('Completed')
        else:
            status.append('Ongoing')

    return JsonResponse({'studyids':study_ids},{'progress':percent_completed},{'status':status})
