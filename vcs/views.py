# vcs/views.py
from django.shortcuts import render, get_object_or_404
from .models import Repository
from django.contrib.auth.decorators import login_required

@login_required
def repository_list(request):
    repositories = Repository.objects.all()
    return render(request, 'vcs/repository_list.html', {'repositories': repositories})

@login_required
def repository_detail(request, pk):
    repository = get_object_or_404(Repository, pk=pk)
    return render(request, 'vcs/repository_detail.html', {'repository': repository})