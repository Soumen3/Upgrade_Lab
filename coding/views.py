from django.shortcuts import render, get_object_or_404
from .models import Problem, TestCase
from .utils import run_code_and_evaluate
import requests
import json

# Create your views here.
def problem_list_view(request):
    # Fetch all problems
    problems = Problem.objects.all()

    # Filter by difficulty (optional)
    difficulty = request.GET.get('difficulty')
    if difficulty:
        problems = problems.filter(difficulty_level=difficulty)

    # Filter by tags (optional)
    tag = request.GET.get('tag')
    if tag:
        problems = problems.filter(tags__icontains=tag)

    context = {'problems': problems}
    return render(request, 'coding/problem_list.html', context)


def problem_detail_view(request, pk):
    context = {}
    problem = get_object_or_404(Problem, pk=pk)

    if request.method == 'POST':
        code = request.POST.get('code')
        language = "python3"  # Assume the language is python
        input_data = problem.sample_input

        # Appwrite function endpoint and API key
        function_endpoint = 'https://cloud.appwrite.io/v1/functions/66f9917400247877f840/executions'
        api_key = 'standard_242521ef0a3caf3a78c2fa57045f5cde4ac1a7d16f7836e4ea591082b86dc3d97e52cdff45c3564d28f8230a0e7d10e93e8a7fb81b85c759b22b58cf1ccb1602241312efa35ff6b8ab755e30802e759aa0e5084d88388fcf9f2a46a8f0eef3bb1f83fe2721f0e550b600fe70a45cb64d73f8693631185f5920a53a0f6345a422'

        payload = {
            'code': code,
            'input': input_data
        }

        headers = {
            'Content-Type': 'application/json',
            'X-Appwrite-Project': '66f83145003403554813',
            'X-Appwrite-Key': api_key
        }

        response = requests.post(function_endpoint, headers=headers, data=json.dumps(payload))
        result = response.json()
        print("result",result)

        context['problem'] = problem
        context['result'] = result.get('output', 'Error running code')
        context['runtime'] = result.get('cpuTime', 'N/A')
        context['memory'] = result.get('memory', 'N/A')

        return render(request, 'coding/problem_detail.html', context)

    context['problem'] = problem
    return render(request, 'coding/problem_detail.html', context)