from django.contrib import admin
from .models import Topic, Question, Option

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # show 4 option fields by default

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('text', 'topic')
    search_fields = ('text',)

admin.site.register(Topic)
admin.site.register(Question, QuestionAdmin)
