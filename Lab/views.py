from django.shortcuts import render
from .ai import ask_chatbot
from django.http import JsonResponse

# Create your views here.
def home(request):
	return render(request, 'Lab/home.html')


def chatbot(request):
    response = "Something went wrong. Please try again."
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = ask_chatbot(prompt, max_tokens=1024)
        return JsonResponse({'response': response})
    return render(request, 'Lab/home.html', {'response': response})