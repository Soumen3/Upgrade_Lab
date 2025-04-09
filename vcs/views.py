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
import io
from icecream import ic
from .utils import parse_gitignore, should_ignore_file
from django.contrib import messages


# ic.disable()

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
    ic(file_structure)
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
                # Check if .gitignore exists in the zip file
                ignore_patterns = []
                gitignore_content = None
                try:
                    for filename in zip_ref.namelist():
                        if filename.endswith('.gitignore'):
                            gitignore_content = zip_ref.read(filename)
                            break
                except Exception as e:
                    # If there's any issue finding .gitignore, continue without it
                    pass
                
                # Parse gitignore patterns (this will include common patterns even if no .gitignore exists)
                ignore_patterns = parse_gitignore(gitignore_content)
                
                # Track processed and ignored files for potential reporting
                processed_files = 0
                ignored_files = 0
                
                # Process files, respecting gitignore patterns
                for zip_info in zip_ref.infolist():
                    if not zip_info.is_dir():
                        # Skip files that match gitignore patterns
                        if should_ignore_file(zip_info.filename, ignore_patterns):
                            ignored_files += 1
                            continue
                            
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
                        processed_files += 1
                
                success_message = f'Repository uploaded successfully. {processed_files} files processed'
                if ignored_files > 0:
                    success_message += f', {ignored_files} files ignored.'
                messages.success(request, success_message)

            return redirect('repository_list')
    else:
        form = RepositoryUploadForm()

    return render(request, 'vcs/upload_repository.html', {'form': form})


@login_required
def file_detail(request, repository_id, file_id):
    file = get_object_or_404(RepositoryFile, repository_id=repository_id, id=file_id)
    return HttpResponse(file.file.read(), content_type='text/plain')

@login_required
def download_repository(request, pk):
    ic("download_repository")
    repository = get_object_or_404(Repository, pk=pk)
    files = RepositoryFile.objects.filter(repository=repository)
    
    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_obj in files:
            # Get file content
            file_content = file_obj.file.read()
            # Add file to zip with its path
            zip_file.writestr(file_obj.path, file_content)
    
    # Prepare response with zip file
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{repository.name}.zip"'
    
    return response

@login_required
def delete_repository(request, pk):
    repository = get_object_or_404(Repository, pk=pk)
    if request.user != repository.owner:
        return HttpResponse("You are not allowed to delete this repository", status=403)
    
    # Get all files associated with the repository
    files = RepositoryFile.objects.filter(repository=repository)
    
    # Delete all files from AWS/S3 storage
    for file_obj in files:
        # This will delete the file from the storage backend (AWS S3)
        if file_obj.file:
            file_obj.file.delete(save=False)
    
    # Delete the repository (and its related objects through CASCADE)
    repository.delete()
    messages.success(request, 'Repository deleted successfully.')
    
    return redirect('repository_list')