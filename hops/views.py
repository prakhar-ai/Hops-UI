from django.shortcuts import render
import requests
import json
from django.http import HttpResponse
from hops.models import OngoingJobs
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home_page(request):
    return render(request,'base.html')

def report(request):
    return render(request,'report.html')

def faqs(request):
    return render(request,'faqs.html')

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def files(request):
    POST = request.POST
    if POST:
        typ = POST['type']
        reason = POST['reason']
        description = POST['description']
        review  = POST['review']
        dicti = {
            'type':typ,
            'reason':reason,
            'description':description,
            'review':review
        }
        dataJSON = dumps(dicti)
        return render(request,'comments.html',{'data':dataJSON})
    else:
        return render(request,'files.html')

def comments(request):
    return render(request,'comments.html')

def vtkviewer(request):
    return render(request,'vtkviewer.html')

def jobs(request):
    data_dict = {}
    study_ids = OngoingJobs.objects.all().values_list('studyid', flat=True) 
    study_ids = list(set(study_ids)) 
    names = OngoingJobs.objects.all().values_list('name', flat=True)
    id = ','.join(study_ids)
    post_data = {'study_instance_ids': str(id)}
    percent_completed = requests.post('http://192.168.1.196:5000/get_progress_percents', data=post_data)
    percent_completed = json.loads(percent_completed.text)['status']
    percent_completed = percent_completed.split(",")
    status = []
    for i in percent_completed:
        if i=="100":
            status.append('Completed')
        else:
            status.append('Ongoing')
    headers = ['Name','Status','Percent Completed']
    rows = []
    for i in range(len(study_ids)):
        row = []
        row.append(study_ids[i])
        row.append(status[i])
        row.append(percent_completed[i])
        row.append(names[i])
        rows.append(row)

    data_dict = {'headers' : headers, 'rows' : rows}
    return render(request,'jobs.html',{'data_dict' : data_dict,'study_ids' : study_ids,'percent_completed': percent_completed})

@csrf_exempt
def getreport(request):
    id = request.POST.get("studyid")
    patient_name = request.POST.get("name")
    jobs = OngoingJobs(studyid=id,name=patient_name)
    jobs.save()
    return JsonResponse({'result' : "Successful",'Name' : patient_name,"Study ID" : id})

def download_report(request,studyid):
    """
    post_data = {'study_instance_id': str(studyid)}
    response_path = requests.post('http://192.168.1.196:5000/get_report', data=post_data)
    path_to_file = response_path.text """
    path_to_file = r"C:\Users\Prakhar\Desktop\1.2.826.0.1.3680043.8.1678.101.10637297040685652766.532213_result.zip"
    response = HttpResponse(content_type='application/zip') 
    with open(path_to_file, 'rb') as fh:  
        response = HttpResponse(fh.read(), content_type='application/zip')   
        response['Content-Disposition'] = 'inline; filename=' + studyid + ".zip"
        return response
    
    