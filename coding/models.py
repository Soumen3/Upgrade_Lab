from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
from django.utils import timezone

# Create your models here.

class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=50, 
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    )
    sample_input = models.JSONField(null=True, blank=True)
    sample_output = models.JSONField(null=True, blank=True)
    explanation = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")

    def __str__(self):
        return self.title

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.JSONField(null=True, blank=True)
    expected_output = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Test Case for {self.problem.title}"
    
class CodeSnippet(models.Model):
    PYTHON = 'python3'
    JAVASCRIPT = 'javascript'
    JAVA = 'java'
    CPP = 'cpp'
    C='c'
    CSHARP = 'csharp'

    LANGUAGE_CHOICES = [
        (PYTHON, 'Python'),
        (JAVASCRIPT, 'JavaScript'),
        (JAVA, 'Java'),
        (CPP, 'C++'),
        (C, 'C'),
        (CSHARP, 'C#'),
    ]

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='code_snippets')
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    code = models.TextField()

    def __str__(self):
        return f"Code Snippet for {self.problem.title} in {self.get_language_display()}"

class Submission(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.CharField(max_length=50, choices=CodeSnippet.LANGUAGE_CHOICES, null=True, blank=True)
    code = models.TextField()
    submission_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=50, 
        choices=[('correct', 'Correct'), ('wrong', 'Wrong Answer'), ('error', 'Runtime Error')]
    )
    runtime = models.FloatField(null=True, blank=True)
    memory = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    problems_solved = models.PositiveIntegerField(default=0)
    ranking = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    solved_problems = models.ManyToManyField(Problem, related_name='solved_by', blank=True)

    def __str__(self):
        return self.user.username


