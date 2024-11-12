from django.shortcuts import render
from .ai import ask_chatbot
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
	return render(request, 'Lab/home.html')

@login_required
def user_profile(request, id, username):
    user=User.objects.get(id=id, username=username)
    if user:
        return render(request, 'Lab/user_profile.html', {'user': user})
    else:
        messages.error(request, 'User not found')
        
    return render(request, 'Lab/home.html')


def chatbot(request):
    response = "Something went wrong. Please try again."
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = ask_chatbot(prompt, max_tokens=1024)
        return JsonResponse({'response': response})
    return render(request, 'Lab/home.html', {'response': response})