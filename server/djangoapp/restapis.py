# Uncomment the imports below before you add the function code
import requests
from urllib.parse import quote
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    request_url = backend_url.rstrip("/") + "/" + endpoint.lstrip("/")
    print("GET from {}".format(request_url))
    try:
        response = requests.get(request_url, params=kwargs, timeout=30)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as exc:
        print("Network or response exception occurred: {}".format(exc))
        return None


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url.rstrip("/") + "/analyze/" + quote(text, safe="")
    try:
        response = requests.get(request_url, timeout=30)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as exc:
        print("Sentiment analysis request failed: {}".format(exc))
        return None


def post_review(data_dict):
    request_url = backend_url.rstrip("/") + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=30)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as exc:
        print("Review submission failed: {}".format(exc))
        return None

