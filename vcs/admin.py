from django.contrib import admin
from .models import Repository, Commit, RepositoryFile

# admin.site.register(Repository)
@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'created_at')
    list_filter = ('owner',)
    search_fields = ('name',)
    readonly_fields = ('id', 'owner', 'created_at')

# admin.site.register(Commit)
@admin.register(Commit)
class CommitAdmin(admin.ModelAdmin):
    list_display = ('id', 'repository', 'message', 'created_at')
    list_filter = ('repository',)
    search_fields = ('message',)
    readonly_fields = ('id', 'repository', 'message', 'created_at')


@admin.register(RepositoryFile)
class RepositoryFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'repository', 'path', 'file')
    list_filter = ('repository',)
    search_fields = ('path',)