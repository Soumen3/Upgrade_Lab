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
    sample_input = models.JSONField()
    sample_output = models.JSONField()
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")

    def __str__(self):
        return self.title

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.JSONField()
    expected_output = models.JSONField()

    def __str__(self):
        return f"Test Case for {self.problem.title}"
    
class CodeSnippet(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='code_snippets')
    language = models.CharField(max_length=50)
    code = models.TextField()

    def __str__(self):
        return f"Code Snippet for {self.problem.title} in {self.language}"

class Submission(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.user.username


