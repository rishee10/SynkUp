from django.db import models

# Create your models here.

from django.db import models

class Job(models.Model):
    JOB_TYPES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('IN', 'Internship'),
        ('CN', 'Contract'),
    ]
    
    WORK_MODES = [
        ('R', 'Remote'),
        ('H', 'Hybrid'),
        ('O', 'On-site'),
    ]
    
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    official_link = models.URLField()
    description = models.TextField()
    requirements = models.TextField()
    skills = models.CharField(max_length=300)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=2, choices=JOB_TYPES)
    work_mode = models.CharField(max_length=1, choices=WORK_MODES)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    application_link = models.URLField()

    def get_skills_list(self):
        return [skill.strip() for skill in self.skills.split(',')]

    def __str__(self):
        return f"{self.title} at {self.company}"