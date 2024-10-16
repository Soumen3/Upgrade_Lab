from django.contrib import admin
from .models import Repository, Commit, RepositoryFile

admin.site.register(Repository)
admin.site.register(Commit)
admin.site.register(RepositoryFile)