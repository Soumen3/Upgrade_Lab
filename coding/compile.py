import boto3
import json
from icecream import ic
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import subprocess
from django.http import JsonResponse
from django.utils import timezone


CODE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'user_codes')

@csrf_exempt
def run_C_code(code, input_data, output_data, language):
    results = []
    total_execution_time = 0
    total_memory_used = 0  # Placeholder for memory usage (if applicable)
    has_error = False  # Flag to track if any error occurs
    error_message = None  # Variable to store the error message

    for test_case, expected_output in zip(input_data, output_data):
        # Unique file name for isolation
        file_id = str(uuid.uuid4())
        file_extension = 'cpp' if language == 'cpp' else 'c'
        file_name = f"{file_id}.{file_extension}"
        file_path = os.path.join(CODE_DIR, file_name)

        # Save the C code to a temporary file
        os.makedirs(CODE_DIR, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(code)

        # Generate the input string for the test case
        input_string = " ".join(str(value) for value in test_case.values())

        # Write the input string to a temporary file
        input_file_name = f"{file_id}_input.txt"
        input_file_path = os.path.join(CODE_DIR, input_file_name)
        with open(input_file_path, 'w') as input_file:
            input_file.write(input_string)

        try:
            # Run Docker command
            start_time = timezone.now()
            compiler = 'g++' if language == 'cpp' else 'gcc'
            cmd = [
                'docker', 'run', '--rm',
                '-v', f'{CODE_DIR}:/app',
                'c-compiler',  # Docker image you created earlier
                'bash', '-c',
                f'{compiler} {file_name} -o {file_id} && timeout 5s ./{file_id} < {input_file_name}'
            ]

            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            end_time = timezone.now()

            output = result.stdout.strip()
            errors = result.stderr.strip()

            # Calculate execution time
            execution_time = (end_time - start_time).total_seconds()
            total_execution_time += execution_time

            # Append results
            results.append({
                "input_set": test_case,
                "actual_output": output,
                "expected_output": expected_output,
                "is_match": str(expected_output) == output,
                "execution_time": execution_time,
                "memory_used": 0,  # Placeholder for memory usage
                "errors": errors if errors else None
            })

            # Set error flag and capture error message if any errors occurred
            if errors:
                has_error = True
                error_message = errors

        except Exception as e:
            has_error = True
            error_message = str(e)
            results.append({
                "input_set": test_case,
                "actual_output": None,
                "expected_output": expected_output,
                "is_match": False,
                "execution_time": 0,
                "memory_used": 0,
                "errors": str(e)
            })

        finally:
            # Cleanup binaries, source files, and input files
            bin_path = os.path.join(CODE_DIR, file_id)
            if os.path.exists(bin_path):
                os.remove(bin_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(input_file_path):
                os.remove(input_file_path)

    # Prepare the result dictionary
    result = {}
    result['body'] = json.dumps({
        "results": results,
        "summary": {
            "average_execution_time": total_execution_time / len(results) if results else 0,
            "average_memory_used": total_memory_used / len(results) if results else 0
        },
        'error': error_message if has_error else None # Initialize error field

    })
    result['statusCode'] = 400 if has_error else 200  # Set status code based on error flag
    # if has_error:
    #     result['body']['error'] = error_message  # Include the error message in the result
    return result



def invoke_lambda_function(function_name, code, input_sets, expected_outputs=None):
    # Create a boto3 client for Lambda
    lambda_client = boto3.client('lambda')
    
    # Prepare the payload with multiple input sets
    payload = {
        'code': code,
        'input_sets': input_sets,
        'expected_outputs': expected_outputs
    }
    
    # Invoke the Lambda function
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,  # The name of the Lambda function
            InvocationType='RequestResponse',  # Synchronous invocation
            Payload=json.dumps(payload)  # Convert payload to JSON string
        )
        
        # Read and parse the response
        response_payload = response['Payload'].read()
        result = json.loads(response_payload)
        
        return result

    except Exception as e:
        return {
            'statusCode': 500,
            'message': 'Error invoking Lambda function',
            'details': str(e)
        }

# Example usage
if __name__ == "__main__":
    # Lambda function name
    function_name = 'javascript-handler'
    
    # Code to be executed by the Lambda function
    code = """
function Solution(inputs) {
    return inputs.a + inputs.b;
}
"""
    
    # Multiple input sets to pass to the 'run' function
    input_sets = [
        {'a': 5, 'b': 3},
        {'a': 10, 'b': 15},
        {'a': -3, 'b': 7}
    ]

    # Expected outputs for each input set
    expected_outputs = [8, 25, 4]

    # Invoke the Lambda function using boto3
    result = invoke_lambda_function(function_name, code, input_sets, expected_outputs)

    # Print the result
    print("Lambda Response:", json.dumps(result, indent=4))

    print("Result: ", json.loads((result['body'])))










