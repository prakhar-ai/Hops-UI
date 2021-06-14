from django.shortcuts import render
import requests
import json
import os
from fpdf import FPDF
from json import dumps
from zipfile import ZipFile
from urllib.request import urlopen
from json import load
from django.http import HttpResponse
from hops.models import OngoingJobs
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

#VPN Username and Password:
#Username:- dermatology
#Password:- XJ8S@DA1$&

WIDTH = 200
HEIGHT = 297

TEST_DATE = "10/20/20"
class PDF(FPDF):
    def header(self):
        self.image("hops_logo.png", 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        self.cell(85)
        self.cell(10, 9, 'Hops Report', 0, 0, 'C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

def create_title(day, pdf):
    pdf.ln(20)
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/2
    data = [['Name','Rahul Jain'],
    ['Age','21'],
    ['Num of lung slices','400'],[
    'Num of positive slices','200'],
    ['ResultType','Abnormal'],
    ['GlobalDiagnosis','Something']
    ]
    th = pdf.font_size
     
    pdf.set_font('Times','B',13.0) 
    pdf.cell(epw, 0.0, 'Date : 08/06/2021', align='L')
    pdf.set_font('Times','',12.0) 
    pdf.ln(2*th)
 
    for row in data:
        for datum in row:
            pdf.cell(col_width, 2*th, str(datum), border=1)
     
        pdf.ln(2*th)
    pdf.ln(2.5*th)

def home_page(request):
    return render(request,'base.html')

def report(request):
    
    studyid = '1.2.826.0.1.3680043.8.1678.101.10637297040685652766.532213_result'
    dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media =os.path.join(dirname, 'media')
    outpath = os.path.join(media,studyid)
    exis = os.path.isfile(outpath)
    
    #print(outpath)
    # for name in zipfile.namelist():    
        # zipfile.extract(name, outpath)
    with ZipFile('1.2.826.0.1.3680043.8.1678.101.10637297040685652766.532213_result.zip', "r") as zipfile:
        arr = zipfile.namelist()
        with zipfile.open(arr[len(arr)-4], "r") as json_file:
            output = load(json_file)
        if not exis:
            zipfile.extractall(outpath)
        dicti = {
            'studyid':studyid,
            'list':arr,
            'out':output
            }
    dataJSON = dumps(dicti)
    
    return render(request,'report.html',{'data':dataJSON,'output': output})

def faqs(request):
    return render(request,'faqs.html')

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def view_2d_images(request):
    #resp = urlopen('https://drive.google.com/uc?export=download&id=1dWUye322dBFsER-O_2yni3z9vBjhcIHh')
    #zipfile = ZipFile(BytesIO(resp.read()))
    #print(zipfile.namelist())
    studyid = '1.2.826.0.1.3680043.8.1678.101.10637297040685652766.532213_result'
    dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media =os.path.join(dirname, 'media')
    outpath = os.path.join(media,studyid)
    exis = os.path.isfile(outpath)
    #print(outpath)
    # for name in zipfile.namelist():    
        # zipfile.extract(name, outpath)
    with ZipFile('1.2.826.0.1.3680043.8.1678.101.10637297040685652766.532213_result.zip', "r") as zipfile:
        if not exis:
            zipfile.extractall(outpath)
        dicti = {
            'studyid':studyid,
            'list':zipfile.namelist()
            }
    dataJSON = dumps(dicti)
    return render(request,'twodimages.html',{'data':dataJSON})


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
        row.append(row.append(OngoingJobs.objects.filter(studyid=study_ids[i])[0].name))
        rows.append(row)

    data_dict = {'headers' : headers, 'rows' : rows}
    return render(request,'jobs.html',{'data_dict' : data_dict,'study_ids' : study_ids,'percent_completed': percent_completed})

@csrf_exempt
def save_to_jobs(request):
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
    path_to_file = r"1.2.826.0.1.3680043.8.1678.101.10637297040685652766.532213_result.zip"
    response = HttpResponse(content_type='application/zip') 
    with open(path_to_file, 'rb') as fh:  
        response = HttpResponse(fh.read(), content_type='application/zip')   
        response['Content-Disposition'] = 'inline; filename=' + studyid + ".zip"
        return response

def download_vti(request):
    studyid = '1.2.826.0.1.3680043.8.1678.101.10637297040685652766.532213_result'
    dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media =os.path.join(dirname, 'media')
    outpath = os.path.join(media,studyid)
    exis = os.path.isfile(outpath)
    #print(outpath)
    # for name in zipfile.namelist():    
        # zipfile.extract(name, outpath)
    with ZipFile('1.2.826.0.1.3680043.8.1678.101.10637297040685652766.532213_result.zip', "r") as zipfile:
        arr = zipfile.namelist()
        if not exis:
            zipfile.extractall(outpath)
        path = os.path.join(outpath,arr[len(arr)-1])
        response = HttpResponse(content_type='application/vti') 
        with open(path, 'rb') as fh:  
            response = HttpResponse(fh.read(), content_type='application/vti')   
            response['Content-Disposition'] = 'inline; filename=' + studyid + ".vti"
    return response

    
def get_report(request):
    day = TEST_DATE
    filename = 'report.pdf'
    pdf = PDF() 
    pdf.add_page()
    create_title(day, pdf)
    pdf.set_draw_color(0, 80, 180)
    pdf.set_fill_color(230, 230, 0)
    pdf.set_text_color(220, 50, 50)
    #zipfile.extractall()
    #print(zipfile.namelist())
    #resp = urlopen('https://drive.google.com/uc?export=download&id=1dWUye322dBFsER-O_2yni3z9vBjhcIHh')
    #zipfile = ZipFile(BytesIO(resp.read()))
    #print(zipfile.namelist())
    studyid = '1.2.826.0.1.3680043.8.1678.101.10637297040685652766.532213_result'
    dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media =os.path.join(dirname, 'media')
    outpath = os.path.join(media,studyid)
    exis = os.path.isfile(outpath)
    #print(outpath)
    # for name in zipfile.namelist():    
        # zipfile.extract(name, outpath)
    with ZipFile('1.2.826.0.1.3680043.8.1678.101.10637297040685652766.532213_result.zip', "r") as zipfile:
        arr = zipfile.namelist()
        if not exis:
            zipfile.extractall(outpath)
    
    pdf.image(os.path.join(outpath,arr[len(arr)-8]), 5, 120, WIDTH/2-10)
    pdf.cell(32)
    pdf.cell(20, 10, 'front', 1, 0 , 'C')
    
    pdf.image(os.path.join(outpath,arr[len(arr)-6]), WIDTH/2, 120, WIDTH/2-10)
    pdf.cell(77)
    pdf.cell(20, 10, 'lateral', 1, 0, 'C')
   
    pdf.image(os.path.join(outpath,arr[len(arr)-5]), 5, 200, WIDTH/2-10)
    pdf.ln(77)
    pdf.cell(32)
    pdf.cell(20, 10, 'natural', 1, 0 , 'C')
       
    pdf.image(os.path.join(outpath,arr[len(arr)-2]), WIDTH/2, 200, WIDTH/2-10)
    pdf.cell(77)
    pdf.cell(20, 10, 'top', 1, 0, 'C')
    result = pdf.output(name = 'filename.pdf', dest = 'F')
    with open('filename.pdf', 'rb') as pdf2:
        response = HttpResponse(pdf2,content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
    return response