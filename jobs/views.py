from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Job
from django.db.models import Q

from django.contrib.auth.decorators import login_required

@login_required
def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    
    # Filtering logic
    job_type = request.GET.get('job_type')
    work_mode = request.GET.get('work_mode')
    location = request.GET.get('location')
    skills = request.GET.get('skills')
    
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if work_mode:
        jobs = jobs.filter(work_mode=work_mode)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if skills:
        skills_list = [s.strip().lower() for s in skills.split(',')]
        query = Q()
        for skill in skills_list:
            query |= Q(skills__icontains=skill)
        jobs = jobs.filter(query)
    
    context = {
        'jobs': jobs,
        'job_types': Job.JOB_TYPES,
        'work_modes': Job.WORK_MODES,
        'selected_filters': {
            'job_type': job_type,
            'work_mode': work_mode,
            'location': location,
            'skills': skills,
        }
    }
    return render(request, 'jobs/job_list.html', context)


login_required
def job_detail(request, pk):
    job = Job.objects.get(pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})