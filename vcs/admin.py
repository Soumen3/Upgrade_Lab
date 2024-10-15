from django.contrib import admin
from .models import Repository, Commit

admin.site.register(Repository)
admin.site.register(Commit)