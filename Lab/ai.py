from decouple import config
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
import markdown
import re

def convert_text_to_html(text):
    lines = text.strip().splitlines()
    html = []
    in_ol = False
    in_ul = False
    in_code_block = False
    code_block_lang = ""

    for line in lines:
        line = line.rstrip()

        # Check for start/end of code block
        if line.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_block_lang = line[3:].strip()
                html.append(f"<pre><code class='{code_block_lang}'>")
            else:
                in_code_block = False
                html.append("</code></pre>")
            continue

        if in_code_block:
            # Escape HTML special characters inside code block
            escaped_line = (
                line.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
            )
            html.append(escaped_line)
            continue

        # Headings
        if re.match(r'^(#{1,6})\s+(.*)', line):
            hashes, content = re.findall(r'^(#{1,6})\s+(.*)', line)[0]
            level = len(hashes)
            html.append(f"<h{level}>{content.strip()}</h{level}>")
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", line):
            if not in_ol:
                html.append("<ol>")
                in_ol = True
            item = re.sub(r"^\d+\.\s+", "", line)
            html.append(f"  <li>{item.strip()}</li>")
            continue
        else:
            if in_ol:
                html.append("</ol>")
                in_ol = False

        # Unordered list
        if re.match(r"^[-*+]\s+", line):
            if not in_ul:
                html.append("<ul>")
                in_ul = True
            item = re.sub(r"^[-*+]\s+", "", line)
            html.append(f"  <li>{item.strip()}</li>")
            continue
        else:
            if in_ul:
                html.append("</ul>")
                in_ul = False

        # Empty line
        if line.strip() == "":
            continue

        # Inline bold and italic
        line = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line)
        line = re.sub(r"\*(.*?)\*", r"<em>\1</em>", line)

        # Inline code
        line = re.sub(r"`(.*?)`", r"<code>\1</code>", line)

        html.append(f"<p>{line}</p>")

    # Close any open list
    if in_ol:
        html.append("</ol>")
    if in_ul:
        html.append("</ul>")
    if in_code_block:
        html.append("</code></pre>")

    return "\n".join(html)


def ask_chatbot(prompt: str, max_tokens: int = 512) -> str:
    # Get the API key from the environment
    api_key = config("HUGGINGFACE_API_KEY")  
    
    template = """<s>[INST]Your name is 'Jarvis'. You are an assistant who helps users with various tasks on our website.
You can intoroduce yourself to the users and provide instructions to assist them. 
You are given a prompt to assist users with tasks such as logging in, registering, writing code, and uploading a repository.
You can solve programming problem also.
[/INST]{question}</s>"""
    
    prompt_template = PromptTemplate.from_template(template)
    formatted_prompt_template = prompt_template.format(
        question=prompt
    )

    # Using the LLaMA 2 model for chat
    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"  # Updated model repository ID
    llm = HuggingFaceEndpoint(
        repo_id=repo_id, 
        huggingfacehub_api_token=api_key,
        temperature=0.7             # Set temperature explicitly
    )

    # Send the prompt and get the response
    response = llm.invoke(formatted_prompt_template, max_tokens=max_tokens)
    response = convert_text_to_html(response)  # Convert markdown to HTML
    return response

# # Example usage
# print(ask_chatbot("How do I register on the website?"))