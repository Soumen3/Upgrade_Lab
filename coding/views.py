from django.shortcuts import render, get_object_or_404
from .models import Problem, TestCase, CodeSnippet
from .utils import invoke_lambda_function
import json
from decouple import config


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
        output_data = problem.sample_output

        # print(code)
        # print(input_data)
        # print(output_data)
        # print(language)

        # Invoke the Lambda function
        function_name = config("LAMBDA_COMPILER_FUNCTION")
        result = invoke_lambda_function(function_name, code, input_data, output_data)

        print("Result: ", json.loads((result['body']))['results'])
        results = json.loads((result['body']))['results']
        summary = json.loads((result['body']))['summary']

        if result['statusCode'] == 200:
            context['result'] = results

        average_execution_time_ms = summary['average_execution_time']
        average_execution_time_s = average_execution_time_ms / 1000.0
        summary['average_execution_time'] = f"{average_execution_time_s:.5f} seconds"

        context['summary'] = summary
        print(summary['average_execution_time'])


    context['problem'] = problem
    code_snippets = CodeSnippet.objects.get(problem=problem)
    context['code_snippets'] = code_snippets


    

    return render(request, 'coding/problem_detail.html', context)