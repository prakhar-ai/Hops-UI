from django.shortcuts import render
import requests
import json
from django.http import HttpResponse
# Create your views here.

def home_page(request):
    return render(request,'base.html')

def training(request):

    return render(request,'training.html')

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

def getreport(request):
    studyid = request.POST.get("studyid")
    post_data = {'study_instance_ids': str(studyid)}
    response = requests.post('http://192.168.1.196:5000/analyze', data=post_data)
    return HttpResponse(response.content)



