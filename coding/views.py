from django.shortcuts import render, get_object_or_404, redirect
from .models import Problem, TestCase, CodeSnippet, Submission
from .utilities import generate_code_snippet, create_or_update_user_profile, handle_run_action, handle_submit_action
from .forms import ProblemForm, TestCaseForm
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse



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
    language = 'python3'

    if request.method == 'POST':
        code = request.POST.get('code')
        action = request.POST.get('action')
        language = request.POST.get('language')  # Get the selected language
        input_data = problem.sample_input
        output_data = problem.sample_output

        context['code'] = code
        context['selected_language'] = language  # Pass the selected language to the context

        if action == 'run':
            try:
                run_context = handle_run_action(code, input_data, output_data, language)
                context.update(run_context)
            except Exception as e:
                messages.error(request, "Something error occured!")
                print("Error: ", e)

        elif action == 'submit':
            try:
                submit_context = handle_submit_action(request.user, problem, code, language)
                context.update(submit_context)
                # print("context: ", context)


                if context.get('error'): 
                    messages.error(request, context['error'])
                # create or update userProfile
                elif context['overall_status'] == 'correct':
                    user_profile = create_or_update_user_profile(request, problem)
                    if user_profile:
                        messages.success(request, 'User Profile Updated Successfully!')
                else:
                    messages.error(request, 'Wrong Answer!')
            except Exception as e:
                messages.error(request, "Something error occured!")
                print("Error: ",e)

    context['problem'] = problem
    if Submission.objects.filter(user=request.user, problem=problem):
        code_snippets = Submission.objects.get(user=request.user, problem=problem, language=language)
    else:
        code_snippets = CodeSnippet.objects.get(problem=problem, language=language)
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

                # generate code snippet for python
                code_snippet = generate_code_snippet(problem_form.cleaned_data['sample_input'])
                CodeSnippet.objects.create(problem=problem, language=code_snippet[1], code=code_snippet[0])

                # generate code snippet for javascript
                code_snippet = generate_code_snippet(problem_form.cleaned_data['sample_input'], language='javascript')
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


def get_code_snippet(request, pk):
    language = request.GET.get('language')
    problem = get_object_or_404(Problem, pk=pk)
    if Submission.objects.filter(user=request.user, problem=problem, language=language):
        code_snippet = Submission.objects.filter(user=request.user, problem=problem, language=language).first()
    else:
        code_snippet = CodeSnippet.objects.filter(problem=problem, language=language).first()
    return JsonResponse({'code': code_snippet.code if code_snippet else ''})
