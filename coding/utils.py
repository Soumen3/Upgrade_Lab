import boto3
import json

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
    function_name = 'test-function'
    
    # Code to be executed by the Lambda function
    code = """
def Solution(a, b):
    return a + b
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