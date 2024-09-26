from django.shortcuts import render, get_object_or_404
from .models import Problem, TestCase
from .utils import run_code_and_evaluate

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

        # Assume you have a function to run the code and evaluate it
        result = run_code_and_evaluate(problem, code)

        context = {'problem': problem, 'result': result}
        return render(request, 'coding/problem_detail.html', context)

    context['problem'] = problem
    return render(request, 'coding/problem_detail.html', context)