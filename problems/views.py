from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from dsa_site import settings
from .models import Problem, TestCase, Submission
from .forms import SubmissionForm

from django.contrib import messages  # Add this import

def home(request):
    return render(request, 'home.html')

@login_required
def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problems_list.html', {'problems': problems})


@login_required
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    visible_test_cases = problem.test_cases.filter(is_visible=True)
    hidden_count = problem.test_cases.filter(is_visible=False).count()
    
    # Get user's previous submissions
    submissions = []
    if request.user.is_authenticated:
        submissions = Submission.objects.filter(user=request.user, problem=problem).order_by('-submission_time')[:5]
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You need to login to submit solutions')
            return redirect('login')
            
        code = request.POST.get('code', '')
        language = request.POST.get('language', 'python')
        
        # Evaluate the submission
        verdict = evaluate_submission(problem, code, language)
        
        # Save submission
        submission = Submission.objects.create(
            user=request.user,
            problem=problem,
            code=code,
            language=language,
            verdict=verdict
        )
        
        messages.success(request, f'Solution {verdict}!')
        return redirect('problem_detail', pk=pk)
    
    return render(request, 'problem_detail.html', {
        'problem': problem,
        'test_cases': visible_test_cases,
        'hidden_count': hidden_count,
        'submissions': submissions,
        'template_code': problem.template_code
    })

def evaluate_submission(problem, code, language):
    # Judge0 API integration
    headers = {
        'x-rapidapi-host': 'judge0-ce.p.rapidapi.com',
        'x-rapidapi-key': settings.JUDGE0_API_KEY,
        'content-type': 'application/json',
    }
    
    # Test against all test cases
    for test_case in problem.test_cases.all():
        data = {
            "source_code": code,
            "language_id": get_language_id(language),
            "stdin": test_case.input,
            "expected_output": test_case.expected_output,
            "cpu_time_limit": problem.time_limit,
        }
        
        response = requests.post(
            f"{settings.JUDGE0_API_URL}/submissions?wait=true",
            json=data,
            headers=headers
        )
        
        result = response.json()
        if result.get('status', {}).get('id') != 3:  # Status 3 = Accepted
            return "Wrong Answer"
    
    return "Accepted"


def get_language_id(language):
    language_map = {
        'python': 71,
        'java': 62,
        'cpp': 54,
        'javascript': 63,
    }
    return language_map.get(language.lower(), 71)  # Default to Python