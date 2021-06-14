from django.shortcuts import render
from django.http import HttpResponse
#import urllib2
from json import load
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import base64
from json import dumps
from .models import Report,Save_report
from fpdf import FPDF
from datetime import datetime, timedelta
import os
from django.conf import settings

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

def training(request):
    return render(request,'training.html')

def prediction(request):
    return render(request,'prediction.html')
'''
def report(request):
    ID = '1'
    try:
        ob = Save_report.objects.get(studyid = ID)
        return render(request,'report.html',{'data':ob.my_data})
    except Exception:
        
        resp = urlopen('https://drive.google.com/uc?export=download&id=1dWUye322dBFsER-O_2yni3z9vBjhcIHh')
        zipfile = ZipFile(BytesIO(resp.read()))
        #print(zipfile.namelist())
        studyid = '1'
        for name in zipfile.namelist():
            mypath = settings.MEDIA_URL
            outpath = os.path.join(mypath,studyid)
            zipfile.extract(name, outpath)
        with zipfile.open('front.png', "r") as image_file:
            front = base64.b64encode(image_file.read()).decode('utf-8')
        with zipfile.open('lateral.png', "r") as image_file:
            lateral = base64.b64encode(image_file.read()).decode('utf-8')
        with zipfile.open('natural.png', "r") as image_file:
            natural = base64.b64encode(image_file.read()).decode('utf-8')
        with zipfile.open('top.png', "r") as image_file:
            top = base64.b64encode(image_file.read()).decode('utf-8')
        with zipfile.open('out.json', "r") as json_file:
            output = load(json_file)
        
        #pdf.output(filename, 'F')
        #print(output)
        dicti = {
            'front':front,
            'lateral':lateral,
            'natural':natural,
            'top':top,
            'output':output
        }
        dataJSON = dumps(dicti)
        Save_report.objects.create(studyid = ID,my_data = dataJSON)
       
        return render(request,'report.html',{'data':dataJSON})
'''

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
'''
def display_images(request):
  
    if request.method == 'GET':
        obs = Report.objects.all() 
        return render((request, 'temp.html',{'images' : obs}))
'''
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
        
"""def zipview(request):
    url = ''
    serialized_data = urllib2.urlopen(url).read()
    data = json.loads(serialized_data)
    return render(request,'temp2.html',{'data':data})
"""



