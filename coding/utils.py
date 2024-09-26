import requests 
import json
import environ

env= environ.Env()
environ.Env.read_env()

def run_code_and_evaluate(code, language, input_data):
    # client_id = env('CLIENT_ID')
    # client_secret = env('CLIENT_SECRET')
    client_id = "d6c0be2fc79d23f0ced828fbbc91fa09"
    client_secret = "28d0f42703b4de51df171ae4a516f8e0b44ea55271041675be9196a68a6b3d43"
    endpoint = 'https://api.jdoodle.com/v1/execute'
    print("code",code)
    
    payload = {
        'clientId': client_id,
        'clientSecret': client_secret,
        'script': code,
        'language': language,  # For example: 'python3', 'cpp', 'java'
        'versionIndex': '3',  # Version index for the specific language
        'stdin': input_data  # Input for the program (if needed)
    }
    
    # Send the POST request to the JDoodle API
    response = requests.post(endpoint, json=payload)

    # Return the result from the API
    return response.json()
