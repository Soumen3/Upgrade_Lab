from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Repository(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.message} - {self.author.username}"

class RepositoryFile(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    file = models.FileField(upload_to='repositories/')
    path = models.CharField(max_length=255)

    def __str__(self):
        return self.path