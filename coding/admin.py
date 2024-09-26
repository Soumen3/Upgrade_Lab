from django.contrib import admin
from .models import Problem, TestCase, Submission, UserProfile

# Register your models here.

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty_level', 'tags')

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('problem',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'status', 'submission_time')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'problems_solved', 'ranking')