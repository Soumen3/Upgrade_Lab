from django.contrib.auth.models import User
from .models import UserProfile
import json
from decouple import config
from django.utils import timezone
from .compile import invoke_lambda_function, run_C_code
from .models import Submission, TestCase
from django.shortcuts import get_object_or_404
from icecream import ic

# ic.disable()

# Generate code snippets for the user post problem:

def generate_python_code(inputs):
    # Generate the Python code snippet based on the input data
    code = f"""# don't change the function name
def Solution({', '.join(inputs[0].keys())}):
    # Write your code here
    
"""
    return code

def generate_javascript_code(inputs):
    # Generate the JavaScript code snippet based on the input data
    code = f"""// don't change the function name
function Solution({', '.join(inputs[0].keys())}) {{
    // Write your code here

}}
"""
    return code

def generate_code_snippet(inputs, language="python3"):
    # Generate the code snippet based on the input data
    if language == "python3":
        code = generate_python_code(inputs)
    elif language == "javascript":
        code = generate_javascript_code(inputs)
        print(code)
    else:
        pass  # Add support for other languages here
    return (code, language)



def create_or_update_user_profile(request, problem):
    if UserProfile.objects.filter(user=request.user).exists():
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.solved_problems.filter(pk=problem.pk).exists():
            return user_profile
        
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
        if problem.difficulty_level == 'easy':
            points = 10
        elif problem.difficulty_level == 'medium':
            points = 20
        else:
            points = 30
        user_profile = UserProfile.objects.create(
            user=request.user,
            problems_solved=1,
            points=points,
        )
        user_profile.solved_problems.add(problem)
        user_profile.save()
    return user_profile


def handle_run_action(code, input_data, output_data, language):
    if language == 'python3':
        function_name = config("LAMBDA_COMPILER_FUNCTION")
        result = invoke_lambda_function(function_name, code, input_data, output_data)
    elif language == 'javascript':
        function_name = config("LAMBDA_COMPILER_FUNCTION_JS")
        result = invoke_lambda_function(function_name, code, input_data, output_data)
    elif language == 'c':
        result = run_C_code(code, input_data, output_data)

    context = {}
    ic(result)

    if result['statusCode'] == 200:
        results = json.loads((result['body']))['results']
        context['result'] = results

        summary = json.loads((result['body']))['summary']
        average_execution_time_ms = summary['average_execution_time']
        average_execution_time_s = average_execution_time_ms / 1000.0
        summary['average_execution_time'] = f"{average_execution_time_s:.5f} seconds"
        context['summary'] = summary
    else:
        context['error'] = json.loads((result['body']))['error']

    return context



def handle_submit_action(user, problem, code, language):
    # Test the code against the single test case
    test_case = get_object_or_404(TestCase, problem=problem)

    input_data = test_case.input_data
    output_data = test_case.expected_output

    if language == 'python3':
        function_name = config("LAMBDA_COMPILER_FUNCTION")
        result = invoke_lambda_function(function_name, code, input_data, output_data)
    elif language == 'javascript':
        function_name = config("LAMBDA_COMPILER_FUNCTION_JS")
        result = invoke_lambda_function(function_name, code, input_data, output_data)
    elif language == 'c':
        result = run_C_code(code, input_data, output_data)

    if result['statusCode'] != 200:
        return {
            'error': json.loads((result['body']))['error']
        }
    
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
        language=language,
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