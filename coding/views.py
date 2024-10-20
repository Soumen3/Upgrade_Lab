from django.shortcuts import render, get_object_or_404, redirect
from .models import Problem, TestCase, CodeSnippet, Submission
from .utils import invoke_lambda_function, generate_code_snippet
from .forms import ProblemForm, TestCaseForm
import json
from decouple import config
from django.contrib import messages
from django.utils import timezone



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
        action = request.POST.get('action')
        language = "python3"  # Assume the language is python
        input_data = problem.sample_input
        output_data = problem.sample_output

        context['code'] = code

        if action == 'run':
            # Invoke the Lambda function for running the code
            function_name = config("LAMBDA_COMPILER_FUNCTION")
            result = invoke_lambda_function(function_name, code, input_data, output_data)

            results = json.loads((result['body']))['results']
            summary = json.loads((result['body']))['summary']

            if result['statusCode'] == 200:
                context['result'] = results

            average_execution_time_ms = summary['average_execution_time']
            average_execution_time_s = average_execution_time_ms / 1000.0
            summary['average_execution_time'] = f"{average_execution_time_s:.5f} seconds"

            context['summary'] = summary

        elif action == 'submit':
            # Test the code against the single test case
            test_case = get_object_or_404(TestCase, problem=problem)

            input_data = test_case.input_data
            expected_output = test_case.expected_output

            function_name = config("LAMBDA_COMPILER_FUNCTION")
            result = invoke_lambda_function(function_name, code, input_data, expected_output)

            results = json.loads((result['body']))['results']
            summary = json.loads((result['body']))['summary']


            print(results)

            overall_status = 'correct' if all(r['is_match'] for r in results) else 'wrong'

            total_execution_time = sum(r['execution_time'] for r in results)
            total_memory_used = sum(r['memory_used'] for r in results)
            average_execution_time = round(total_execution_time / len(results), 5)
            average_memory_used = total_memory_used / len(results)

            # Get or create the submission
            submission, created = Submission.objects.get_or_create(
                user=request.user,
                problem=problem,
                defaults={'code': code}
            )

            # Update the submission fields
            submission.code = code
            submission.status = overall_status
            submission.runtime = average_execution_time
            submission.memory = average_memory_used
            submission.submission_time = timezone.now()  # Update the submission time
            submission.save()

            context['submission'] = submission
            context['all_results'] = results


    context['problem'] = problem
    if Submission.objects.filter(user=request.user, problem=problem):
        code_snippets = Submission.objects.get(user=request.user, problem=problem)
    else:
        code_snippets = CodeSnippet.objects.get(problem=problem)
    context['code_snippets'] = code_snippets

    return render(request, 'coding/problem_detail.html', context)


def post_problems(request):
    if request.method == 'POST':
        print("POST request received")
        problem_form = ProblemForm(request.POST)
        testcase_form = TestCaseForm(request.POST)

        if problem_form.is_valid() and testcase_form.is_valid():
            if request.user.groups.filter(name='problems_manager').exists():
                problem = problem_form.save()
                testcase = testcase_form.save(commit=False)
                testcase.problem = problem
                testcase.save()
                code_snippet = generate_code_snippet(problem_form.cleaned_data['sample_input'])
                CodeSnippet.objects.create(problem=problem, language=code_snippet[1], code=code_snippet[0])
                messages.success(request, 'Problem posted successfully!')
                return redirect('post_problem')
            else:
                print("User does not have permission to post problems")
                messages.error(request, 'You do not have permission to post problems.')
        else:
            print("Form is invalid")
            messages.error(request, 'Error postin the problem! Invalid form data.')

    else:
        problem_form = ProblemForm()
        testcase_form = TestCaseForm()

    context = {
        'problem_form': problem_form,
        'testcase_form': testcase_form,
    }
    return render(request, 'coding/post_problem.html', context)