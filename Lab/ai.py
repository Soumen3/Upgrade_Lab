from decouple import config
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

def ask_chatbot(prompt: str, max_tokens: int = 512) -> str:
    # Get the API key from the environment
    api_key = config("HUGGINGFACE_API_KEY")

    template = """<s>[INST]Your name is 'Jarvis'. You are an assistant who helps users with various tasks on our website. 
        You are given a prompt to assist users with tasks such as logging in, registering, writing code, and uploading a repository.
        You need to provide detailed instructions based on the prompt.
        If any prompt is not related to these tasks, you must ignore it.
        Even you must not give a hint about the unrelated prompt.
        </s>{question}[/INST]"""
    
    prompt_template = PromptTemplate.from_template(template)
    formatted_prompt_template = prompt_template.format(
        question = prompt
    )

    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
    llm = HuggingFaceEndpoint(repo_id = repo_id, huggingfacehub_api_token = api_key)

    response = llm.invoke(formatted_prompt_template, max_tokens=max_tokens)
    return response

