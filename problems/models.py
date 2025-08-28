from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

from dsa_site import settings

User = get_user_model()

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    ]
    template_code = models.TextField(
        blank=True,
        default="""def solution(input):\n    # Write your code here\n    return""",
        help_text="Initial code template to display in the editor"
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_limit = models.IntegerField(default=2)  # in seconds
    memory_limit = models.IntegerField(default=256)  # in MB

    def __str__(self):
        return self.title

# class TestCase(models.Model):
#     problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
#     input = models.TextField()
#     output = models.TextField()
#     is_visible = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Test case for {self.problem.title}"


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input = models.TextField()
    expected_output = models.TextField()
    is_visible = models.BooleanField(
        default=True,
        help_text="Should this test case be visible to users?"
    )
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"Test case for {self.problem.title} (Visible: {self.is_visible})"


class Submission(models.Model):
    VERDICT_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Wrong Answer', 'Wrong Answer'),
        ('Time Limit Exceeded', 'Time Limit Exceeded'),
        ('Runtime Error', 'Runtime Error'),
    ]
    
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('javascript', 'JavaScript'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    verdict = models.CharField(max_length=20, choices=VERDICT_CHOICES)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s submission for {self.problem.title}"