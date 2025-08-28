from django.shortcuts import render, get_object_or_404
from .models import Topic, Question

from django.contrib.auth.decorators import login_required

@login_required
def topic_list(request):
    topics = Topic.objects.all()
    return render(request, 'aptitude/topic_list.html', {'topics': topics})

@login_required
def question_list(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    questions = topic.questions.prefetch_related('options').all()
    return render(request, 'aptitude/question_list.html', {
        'topic': topic,
        'questions': questions
    })
