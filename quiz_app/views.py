from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Topic, Question, QuizResult, UserAnswer

import random

@login_required
def topic_selection(request):
    topics = Topic.objects.all()
    return render(request, 'quiz/topic_selection.html', {'topics': topics})


# @login_required
# def feedback_detail(request, result_id):
#     result = get_object_or_404(QuizResult, pk=result_id, user=request.user)
#     answers = result.useranswer_set.all()
#     return render(request, 'quiz/feedback.html', {
#         'result': result,
#         'answers': answers
#     })

@login_required
def result_detail(request, result_id):
    result = get_object_or_404(QuizResult, pk=result_id, user=request.user)
    answers = UserAnswer.objects.filter(result=result).select_related('question')
    
    return render(request, 'quiz/result_detail.html', {
        'result': result,
        'answers': answers,
        'score_percentage': result.score,
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Topic, Question, QuizResult, UserAnswer
from .utils import compare_answers
import random

@login_required
def start_quiz(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    questions = list(Question.objects.filter(topic=topic))
    
    if not questions:
        return redirect('quiz_app:topic_selection')
    
    random.shuffle(questions)
    request.session['quiz_data'] = {
        'topic_id': topic.id,
        'questions': [q.id for q in questions],
        'current_index': 0,
        'answers': []
    }
    return redirect('quiz_app:question_view')


@login_required
def question_view(request):
    quiz_data = request.session.get('quiz_data')
    if not quiz_data:
        return redirect('quiz_app:topic_selection')
    
    current_index = quiz_data['current_index']
    if current_index >= len(quiz_data['questions']):
        return redirect('quiz_app:process_results')
    
    question = get_object_or_404(Question, pk=quiz_data['questions'][current_index])
    
    return render(request, 'quiz/question.html', {
        'question': question,
        'time_limit': question.get_time_limit(),
        'question_number': current_index + 1,
        'total_questions': len(quiz_data['questions'])
    })
        

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@login_required
@csrf_exempt  # Temporary for debugging
def save_answer(request):
    quiz_data = request.session.get('quiz_data')
    if not quiz_data:
        return JsonResponse({'status': 'error', 'message': 'No active quiz'}, status=400)

    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        answer_text = data.get('answer_text', '').strip()
        is_auto_submitted = data.get('time_expired', False)

        quiz_data['answers'].append({
            'question_id': int(question_id),
            'answer_text': answer_text,
            'is_auto_submitted': is_auto_submitted
        })
        
        quiz_data['current_index'] += 1
        request.session['quiz_data'] = quiz_data
        request.session.modified = True  # Critical for session saving
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)





@login_required
def process_results(request):
    quiz_data = request.session.get('quiz_data')
    if not quiz_data or not quiz_data.get('answers'):
        return redirect('quiz_app:topic_selection')
    
    topic = get_object_or_404(Topic, pk=quiz_data['topic_id'])
    total_score = 0
    
    # Create quiz result
    result = QuizResult.objects.create(
        user=request.user,
        topic=topic,
        score=0
    )
    
    # Process each answer
    for answer_data in quiz_data['answers']:
        question = get_object_or_404(Question, pk=answer_data['question_id'])
        
        if answer_data.get('is_auto_submitted'):
            # Auto-submitted (timed out) answer
            UserAnswer.objects.create(
                result=result,
                question=question,
                user_answer='',
                similarity_score=0,
                feedback="Time expired - no answer submitted",
                is_auto_submitted=True
            )
        else:
            # User-submitted answer
            similarity, feedback = compare_answers(
                answer_data['answer_text'],
                question.ideal_answer
            )
            UserAnswer.objects.create(
                result=result,
                question=question,
                user_answer=answer_data['answer_text'],
                similarity_score=similarity,
                feedback=feedback,
                is_auto_submitted=False
            )
            total_score += similarity
    
    # Calculate final score (0-100 scale)
    if quiz_data['answers']:
        final_score = (total_score / len(quiz_data['answers'])) * 100
    else:
        final_score = 0
    
    result.score = final_score
    result.save()
    
    # Get all answers with related questions
    answers = result.useranswer_set.all().select_related('question')
    
    return render(request, 'quiz/result.html', {
        'result': result,
        'answers': answers
    })