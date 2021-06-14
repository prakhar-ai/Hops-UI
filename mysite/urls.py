"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hops.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', files),
    path('faqs',faqs),
    path('comments',comments),
    path('vtkviewer',vtkviewer),
    path('jobs',jobs),
    path('files',files),
    path('login',login),
    path('register',register),
    path('report',report),   
    path('save_to_jobs',save_to_jobs,name='save_to_jobs'),  
    path('view_2d_images',view_2d_images),
    path('getreport',get_report),
    path('download_report/<str:studyid>',download_report,name='download_report'),
    path('download_vti',download_vti),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)