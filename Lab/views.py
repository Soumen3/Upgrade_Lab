from django.shortcuts import render, get_object_or_404, redirect
from .ai import ask_chatbot
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import UserDetailForm
from .models import UserDetail, socialMedia
from vcs.models import Repository
from coding.models import UserProfile
from .utils import get_user_all_detail_filled, get_social_media_filled

# Create your views here.
def home(request):
	return render(request, 'Lab/home.html')

@login_required
def user_profile(request, id, username):
    context = {}
    user = get_object_or_404(User, id=id, username=username)
    context['user_profile'] = user
    try:
        # Fix: Unpack the tuple returned by get_or_create
        user_detail, created = UserDetail.objects.get_or_create(user=user)
        repositories = Repository.objects.filter(owner=user)
        context['repositories']=repositories
        user_profile_details = UserProfile.objects.get(user=user)
        solved_problems = user_profile_details.solved_problems.all()
        context['solved_problems'] = solved_problems
        social_media, social_created=socialMedia.objects.get_or_create(user=user_detail)
        context['social_media']=social_media

    except UserDetail.DoesNotExist:
        user_detail = None
    context['user_detail'] = user_detail
    context.update(get_user_all_detail_filled(user))
    context.update(get_social_media_filled(user))
    if user:
        return render(request, 'Lab/user_profile.html', context)
    else:
        messages.error(request, 'User not found')
    return render(request, 'Lab/home.html')

@login_required
def add_user_detail(request, id, username):
    # Check if the user already has a UserDetail
    if request.user.id != id:
        messages.error(request, 'You can only update your own profile')
        return redirect('home')
    
    # Get or create UserDetail
    user_detail, created = UserDetail.objects.get_or_create(user=request.user)
    
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
    
    return redirect('user_profile', id=id, username=username)

@login_required
def update_social_media(request, id, username):
    user, created= User.objects.get_or_create(id=id, username=username)

    print("hello")
    # Ensure the logged-in user is only updating their own profile
    if request.user != user:
        messages.error(request, 'You can only update your own social media information.')
        return redirect('home')
    
    if request.method == 'POST':
        # Fix: Unpack the tuple returned by get_or_create
        user_detail, detail_created = UserDetail.objects.get_or_create(user=user)
        
        # Get or create social media object
        social_media, created = socialMedia.objects.get_or_create(user=user_detail)
        
        # Update fields
        social_media.github_username = request.POST.get('github_username', '')
        social_media.linkedin_username = request.POST.get('linkedin_username', '')
        social_media.twitter_username = request.POST.get('twitter_username', '')
        social_media.facebook_username = request.POST.get('facebook_username', '')
        social_media.instagram_username = request.POST.get('instagram_username', '')
        
        social_media.save()
        
        messages.success(request, 'Social media information updated successfully.')
        
    return redirect('user_profile', id=id, username=username)

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