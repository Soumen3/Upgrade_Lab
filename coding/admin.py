from django.contrib import admin
from .models import Problem, TestCase, Submission, UserProfile, CodeSnippet

# Register your models here.

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty_level', 'tags')

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('problem',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'status', 'submission_time', 'runtime', 'memory')
    list_filter = ('status', 'submission_time')
    search_fields = ('user__username', 'problem__title')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'problems_solved', 'ranking')

@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ('problem', 'language', 'code')