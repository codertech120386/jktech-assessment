import subprocess

from fastapi import status

from src.utils import generic_response


def run_ollama(model: str, prompt: str):
    # Build the command
    command = ['ollama', 'run', model, prompt]

    # Running the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        return result.stdout


def generate_summary_using_llama3(content: str):
    model = "llama3"
    prompt = f"text: {content}\nGive a short summary in 4-5 paragraphs for the above text"

    try:
        response = run_ollama(model, prompt)
        return generic_response({"data": response, "status_code": status.HTTP_200_OK})
    except Exception as e:
        print(e)
        return generic_response(
            {"message": "Something went wrong .. please try again later",
             "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})
