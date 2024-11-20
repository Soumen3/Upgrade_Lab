from django.shortcuts import render, get_object_or_404, redirect
from .ai import ask_chatbot
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import UserDetailForm
from .models import UserDetail
from vcs.models import Repository

# Create your views here.
def home(request):
	return render(request, 'Lab/home.html')

# @login_required
def user_profile(request, id, username):
    context = {}
    user = get_object_or_404(User, id=id, username=username)
    context['user_profile'] = user
    try:
        user_detail = UserDetail.objects.get(user=user)
    except UserDetail.DoesNotExist:
        user_detail = None
    context['user_detail'] = user_detail
    if user:
        return render(request, 'Lab/user_profile.html', context)
    else:
        messages.error(request, 'User not found')
    return render(request, 'Lab/home.html')

@login_required
def add_user_detail(request, id, username):
    # Check if the user already has a UserDetail
    user_detail = UserDetail.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = UserDetailForm(request.POST, request.FILES, instance=user_detail)
        if form.is_valid():
            user_detail = form.save(commit=False)
            user_detail.user = request.user  # Ensure user is assigned
            user_detail.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('user_profile', id=request.user.id, username=request.user.username)
        else:
            messages.error(request, 'Profile update failed')

    else:
        # If no UserDetail exists for the user, create an empty form
        if not user_detail:
            form = UserDetailForm()
        else:
            # If a UserDetail exists, pass the existing object to the form
            form = UserDetailForm(instance=user_detail)

    return render(request, 'Lab/add_user_detail.html', {'form': form})

def chatbot(request):
    response = "Something went wrong. Please try again."
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = ask_chatbot(prompt, max_tokens=1024)
        return JsonResponse({'response': response})
    return render(request, 'Lab/home.html', {'response': response})




def search(request):
    query = request.GET.get('query')
    repositories = None
    users = None

    if query:
        repositories = Repository.objects.filter(name__icontains=query)
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(userdetail__institute__icontains=query)
        )
        users = users.distinct()
        

    context = {
        'repositories': repositories,
        'users': users,
        'query': query,
    }
    return render(request, 'Lab/search_results.html', context)