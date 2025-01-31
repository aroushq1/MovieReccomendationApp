import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@api_view(['GET'])
def fetch_movies(request):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    return Response(response.json())

@api_view(['GET'])
def search_movies(request, query):
    url = f"https://api.themoviedb.org/3/search/movie?query={query}&api_key={TMDB_API_KEY}"
    response = requests.get(url)
    return Response(response.json())

@api_view(['POST'])
def get_recommendations(request):
    user_input = request.data.get("movies", [])
    prompt = f"Suggest 5 movies similar to {', '.join(user_input)}"

    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
    response = requests.post(
        "https://api.gemini.ai/v1/completions",
        json={"model": "gemini-pro", "prompt": prompt, "max_tokens": 100},
        headers=headers,
    )
    return Response(response.json())
