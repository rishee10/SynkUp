# from django.contrib import admin

# # Register your models here.
# from django.contrib import admin
# from .models import Problem, TestCase, Submission

# class TestCaseInline(admin.TabularInline):
#     model = TestCase
#     extra = 1

# class ProblemAdmin(admin.ModelAdmin):
#     inlines = [TestCaseInline]
#     list_display = ('title', 'difficulty', 'created_at')
#     list_filter = ('difficulty', 'created_at')
#     search_fields = ('title', 'description')

# admin.site.register(Problem, ProblemAdmin)
# admin.site.register(Submission)

from django.contrib import admin
from django import forms

from problems.models import Problem, Submission, TestCase

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = '__all__'

    def clean_is_visible(self):
        problem = self.cleaned_data.get('problem')
        is_visible = self.cleaned_data.get('is_visible')
        
        if problem and problem.test_cases.count() < 2 and not is_visible:
            raise forms.ValidationError("First 2 test cases must be visible to users")
        return is_visible

class TestCaseInline(admin.TabularInline):
    model = TestCase
    form = TestCaseForm
    extra = 1
    fields = ('input', 'expected_output', 'is_visible', 'explanation')
    ordering = ('id',)  # Ensure consistent ordering

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('id')  # Important for consistent numbering

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [TestCaseInline]
    save_on_top = True

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        # Ensure first 2 test cases are visible
        for i, instance in enumerate(instances):
            if i < 2:
                instance.is_visible = True
            instance.save()
        formset.save_m2m()

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'language', 'verdict', 'submission_time')
    list_filter = ('verdict', 'language', 'submission_time')