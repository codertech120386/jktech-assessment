import subprocess

from fastapi import status
from icecream import ic

from src.utils import generic_response
from src.books.service import fetch_latest_rating_given_by_user
from database import SessionLocal

from .service import machine_learning_recommendations


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


def get_recos(user_id: int, session: SessionLocal):
    try:
        rating_genre = fetch_latest_rating_given_by_user(user_id=user_id, session=session)
        if not rating_genre:
            return generic_response(
                {"error": True, "message": "No Recommendations yet", "status_code": status.HTTP_400_BAD_REQUEST})
        recommendation = machine_learning_recommendations(rating=rating_genre["rating"], genre=rating_genre["genre"])

        return generic_response({"data": recommendation, "status_code": status.HTTP_201_CREATED})
    except Exception as e:
        print(e)
        return generic_response(
            {"message": "Something went wrong .. please try again later",
             "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})
