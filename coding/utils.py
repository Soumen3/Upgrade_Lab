import subprocess

import subprocess

def run_code_and_evaluate(problem, code):
    # For simplicity, assuming Python code (adjust for other languages)
    with open('user_code.py', 'w') as f:
        f.write(code)

    # Run the user code and capture the output
    try:
        result = subprocess.run(
            ['python', 'user_code.py'], 
            input=problem.sample_input,  # Pass the input to the subprocess
            capture_output=True, 
            text=True, 
            timeout=5  # Prevent infinite loops
        )
        # Compare result with expected output from test cases
        print("result:", result.stdout.strip())
        print(problem.sample_output.strip())
        if result.stdout.strip() == problem.sample_output.strip():
            return "Correct"
        else:
            return "Wrong Answer"
    except subprocess.TimeoutExpired:
        return "Timeout Error"
    except subprocess.CalledProcessError:
        return "Runtime Error"
