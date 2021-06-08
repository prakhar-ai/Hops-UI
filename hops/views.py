from django.shortcuts import render
#import urllib2
from json import load
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import base64
from json import dumps
from .models import Report,Save_report

# Create your views here.
#VPN Username and Password:
#Username:- dermatology
#Password:- XJ8S@DA1$&

def home_page(request):
    return render(request,'base.html')

def training(request):
    return render(request,'training.html')

def prediction(request):
    return render(request,'prediction.html')

def report(request):
    ID = '1.2.826.0.1.3680043.8.1678.101.10637203703447639663.147272'
    try:
        ob = Save_report.objects.get(studyid = ID)
        return render(request,'report.html',{'data':ob.my_data})
    except Exception:
        resp = urlopen('https://drive.google.com/uc?export=download&id=1dWUye322dBFsER-O_2yni3z9vBjhcIHh')
        zipfile = ZipFile(BytesIO(resp.read()))
        #print(zipfile.namelist())
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

def display_images(request):
  
    if request.method == 'GET':
        obs = Report.objects.all() 
        return render((request, 'temp.html',{'images' : obs}))
        
"""def zipview(request):
    url = ''
    serialized_data = urllib2.urlopen(url).read()
    data = json.loads(serialized_data)
    return render(request,'temp2.html',{'data':data})
"""



