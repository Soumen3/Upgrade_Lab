from django.shortcuts import render, get_list_or_404, get_object_or_404
from .ai import ask_chatbot
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserDetailForm
from .models import UserDetail

# Create your views here.
def home(request):
	return render(request, 'Lab/home.html')

@login_required
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
    if request.method == 'POST':
        form = UserDetailForm(request.POST, request.FILES)
        if form.is_valid():
            user_detail = form.save(commit=False)
            user_detail.user = request.user
            user_detail.save()
            messages.success(request, 'Profile updated successfully')
            return render(request, 'Lab/user_profile.html', {'user': request.user})
        else:
            messages.error(request, 'Profile update failed')
    else:
        user_detail=get_object_or_404(UserDetail, user=request.user)
        if user_detail:
            form = UserDetailForm(instance=user_detail)
        else:
            form = UserDetailForm()
    return render(request, 'Lab/add_user_detail.html', {'form': form})

def chatbot(request):
    response = "Something went wrong. Please try again."
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = ask_chatbot(prompt, max_tokens=1024)
        return JsonResponse({'response': response})
    return render(request, 'Lab/home.html', {'response': response})