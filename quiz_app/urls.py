from django.urls import path
from . import views

app_name = 'quiz_app'

from django.urls import path
from . import views

app_name = 'quiz_app'

urlpatterns = [
    path('', views.topic_selection, name='topic_selection'),
    path('start/<int:topic_id>/', views.start_quiz, name='start_quiz'),
    path('question/', views.question_view, name='question_view'),
    path('save-answer/', views.save_answer, name='save_answer'),
    path('results/', views.process_results, name='process_results'),
]