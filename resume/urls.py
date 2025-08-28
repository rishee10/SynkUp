from django.contrib import admin
from django.urls import path

from resume.views import gen_resume, rhome
# app_name = 'resume'

urlpatterns = [
    path('', rhome, name = 'rhome'), 
    path('resume/', gen_resume, name = 'resume'),
    
]