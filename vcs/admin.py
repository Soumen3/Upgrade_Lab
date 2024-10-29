from django.contrib import admin
from .models import Repository, Commit, RepositoryFile

admin.site.register(Repository)
admin.site.register(Commit)


@admin.register(RepositoryFile)
class RepositoryFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'repository', 'path', 'file')
    list_filter = ('repository',)
    search_fields = ('path',)