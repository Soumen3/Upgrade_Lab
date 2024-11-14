from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Repository, RepositoryFile
from .form import RepositoryUploadForm
import zipfile
from pathlib import Path
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.contrib.auth.models import User


@login_required
def repository_list(request):
    repositories = Repository.objects.filter(owner=request.user)
    return render(request, 'vcs/repository_list.html', {'repositories': repositories})

@login_required
def repository_detail(request, pk):
    context = {}
    repository = get_object_or_404(Repository, pk=pk)
    context['repository'] = repository
    files = RepositoryFile.objects.filter(repository=repository)
    file_structure = build_file_structure(files)
    context['files'] = file_structure
    return render(request, 'vcs/repository_detail.html', context)

def build_file_structure(files):
    file_structure = {}
    for file in files:
        parts = file.path.split('/')
        current_level = file_structure
        for part in parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        current_level[parts[-1]] = file
    print(file_structure)
    return file_structure

@login_required
def upload_repository(request):
    if request.method == 'POST':
        form = RepositoryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            file = request.FILES['file']

            # Save the repository information to the database
            repository = Repository(name=name, description=description, owner=request.user)
            repository.save()

            # Extract the zip file and save the files to S3
            with zipfile.ZipFile(file, 'r') as zip_ref:
                for zip_info in zip_ref.infolist():
                    if not zip_info.is_dir():
                        # Extract the file content
                        extracted_file = zip_ref.read(zip_info)
                        s3_file = ContentFile(extracted_file)
                        s3_file.name = f'{repository.owner}/{repository.id}/{zip_info.filename}'

                        # Save the file information to the database
                        RepositoryFile.objects.create(
                            repository=repository,
                            file=s3_file,
                            path=zip_info.filename
                        )

            return redirect('repository_list')
    else:
        form = RepositoryUploadForm()

    return render(request, 'vcs/upload_repository.html', {'form': form})



@login_required
def file_detail(request, repository_id, file_id):
    file = get_object_or_404(RepositoryFile, repository_id=repository_id, id=file_id)
    return HttpResponse(file.file.read(), content_type='text/plain')