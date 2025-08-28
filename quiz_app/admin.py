from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Topic, Question, QuizResult, UserAnswer

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'question_count')
    
    def question_count(self, obj):
        return obj.question_set.count()
    question_count.short_description = 'Questions'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'difficulty')
    list_filter = ('topic', 'difficulty')
    search_fields = ('text', 'ideal_answer')

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    readonly_fields = ('question', 'user_answer', 'similarity_score', 'feedback')
    extra = 0

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'score', 'created_at')
    list_filter = ('topic', 'created_at')
    inlines = [UserAnswerInline]
    readonly_fields = ('user', 'topic', 'score')
