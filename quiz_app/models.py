from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from dsa_site import settings

from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy (10 sec)'),
        ('medium', 'Medium (14 sec)'),
        ('hard', 'Hard (15 sec)'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    ideal_answer = models.TextField()
    
    def get_time_limit(self):
        return {
            'easy': 10,
            'medium': 14,
            'hard': 15
        }.get(self.difficulty, 10)

class QuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s {self.topic.name} result"

class UserAnswer(models.Model):
    result = models.ForeignKey(QuizResult, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.TextField()
    similarity_score = models.FloatField()
    feedback = models.TextField()
    is_auto_submitted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['id']  # Maintain question order