from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

# class CustomUser(AbstractUser):
#     score = models.IntegerField(default=0)
#     problems_solved = models.IntegerField(default=0)
    
#     def __str__(self):
#         return self.username

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    score = models.IntegerField(default=0)
    problems_solved = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username