from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=50, 
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    )
    problem_statement = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")

    def __str__(self):
        return self.title

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()

    def __str__(self):
        return f"Test Case for {self.problem.title}"

class Submission(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    submission_time = models.DateTimeField(auto_now_add=True)
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
