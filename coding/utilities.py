from django.contrib.auth.models import User
from .models import UserProfile
import json
from decouple import config
from django.utils import timezone
from .compile import invoke_lambda_function
from .models import Submission, TestCase
from django.shortcuts import get_object_or_404


# Generate code snippets for the user post problem:

def generate_python_code(inputs):
    # Generate the Python code snippet based on the input data
    code = f"""
def Solution({', '.join(inputs[0].keys())}):
    # Write your code here
    
"""
    return code

def generate_code_snippet(inputs, language="python3"):
    # Generate the code snippet based on the input data
    if language == "python3":
        code = generate_python_code(inputs)
    else:
        pass  # Add support for other languages here
    return (code, language)




def create_or_update_user_profile(request, problem):
    if UserProfile.objects.filter(user=request.user).exists():
        user_profile = UserProfile.objects.get(user=request.user)
        if problem.difficulty_level == 'easy':
            user_profile.points += 10
        elif problem.difficulty_level == 'medium':
            user_profile.points += 20
        else:
            user_profile.points += 30

        user_profile.solved_problems.add(problem)
        user_profile.problems_solved = user_profile.solved_problems.count()
        user_profile.save()
    else:
        user_profile = UserProfile.objects.create(
            user=request.user,
            problems_solved=1,
            points=10,
        )
        user_profile.solved_problems.add(problem)
        user_profile.save()
    return user_profile


def handle_run_action(code, input_data, output_data):
    function_name = config("LAMBDA_COMPILER_FUNCTION")
    result = invoke_lambda_function(function_name, code, input_data, output_data)

    results = json.loads((result['body']))['results']
    summary = json.loads((result['body']))['summary']

    context = {}
    if result['statusCode'] == 200:
        context['result'] = results
    else:
        context['error'] = results

    average_execution_time_ms = summary['average_execution_time']
    average_execution_time_s = average_execution_time_ms / 1000.0
    summary['average_execution_time'] = f"{average_execution_time_s:.5f} seconds"

    context['summary'] = summary

    return context



def handle_submit_action(user, problem, code):
    # Test the code against the single test case
    test_case = get_object_or_404(TestCase, problem=problem)

    input_data = test_case.input_data
    output_data = test_case.expected_output

    function_name = config("LAMBDA_COMPILER_FUNCTION")
    result = invoke_lambda_function(function_name, code, input_data, output_data)

    results = json.loads((result['body']))['results']
    summary = json.loads((result['body']))['summary']
    overall_status = 'correct' if all(r['is_match'] for r in results) else 'wrong'

    total_execution_time = sum(r['execution_time'] for r in results)
    total_memory_used = sum(r['memory_used'] for r in results)
    average_execution_time = round(total_execution_time / len(results), 5)
    average_memory_used = total_memory_used / len(results)

    # Get or create the submission
    submission, created = Submission.objects.get_or_create(
        user=user,
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

    context = {
        'submission': submission,
        'all_results': results,
        'overall_status': overall_status,
    }

    return context