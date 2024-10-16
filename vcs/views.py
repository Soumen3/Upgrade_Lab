from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Repository, RepositoryFile
from .form import RepositoryUploadForm
import zipfile
import os
from pathlib import Path
from django.core.files.base import ContentFile


@login_required
def repository_list(request):
    repositories = Repository.objects.filter(owner=request.user)
    return render(request, 'vcs/repository_list.html', {'repositories': repositories})

@login_required
def repository_detail(request, pk):
    repository = get_object_or_404(Repository, pk=pk)
    files = RepositoryFile.objects.filter(repository=repository)
    return render(request, 'vcs/repository_detail.html', {'repository': repository, 'files': files})

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

            # Extract the zip file and save the files to the local storage
            with zipfile.ZipFile(file, 'r') as zip_ref:
                for zip_info in zip_ref.infolist():
                    if not zip_info.is_dir():
                        # Create the full path for the file
                        full_path = Path(settings.MEDIA_ROOT) / 'repositories' / str(repository.owner) / str(repository.id) / zip_info.filename
                        full_path.parent.mkdir(parents=True, exist_ok=True)  # Create directories if they don't exist

                        # Extract the file content
                        extracted_file = zip_ref.read(zip_info)
                        with open(full_path, 'wb') as f:
                            f.write(extracted_file)

                        # Save the file information to the database
                        RepositoryFile.objects.create(
                            repository=repository,
                            file=full_path.relative_to(settings.MEDIA_ROOT).as_posix(),
                            path=zip_info.filename
                        )

            return redirect('repository_list')

    form = RepositoryUploadForm()

    return render(request, 'vcs/upload_repository.html', {'form': form})