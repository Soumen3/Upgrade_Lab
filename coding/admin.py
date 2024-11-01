from django.contrib import admin
from .models import Problem, TestCase, Submission, UserProfile, CodeSnippet

# Register your models here.

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'difficulty_level', 'tags')

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem','language', 'status', 'submission_time', 'runtime', 'memory')
    list_filter = ('status', 'submission_time')
    search_fields = ('user__username', 'problem__title')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problems_solved', 'ranking')

@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'language', 'code')