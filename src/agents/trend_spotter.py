"""
Trend-Spotter Node: Researches global film trends from free data sources
"""

import requests
from typing import Dict, Any
from ..config import TMDB_API_KEY


def get_global_trends() -> Dict[str, Any]:
    """
    Research global film trends from TMDB API.
    
    Returns:
        dict: Contains trending films with title, genre, rating, etc.
    """
    try:
        # TMDB endpoint for trending movies
        url = "https://api.themoviedb.org/3/trending/movie/week"
        
        # Use Bearer Token authentication
        headers = {
            "Authorization": f"Bearer {TMDB_API_KEY}",
            "accept": "application/json"
        }
        
        params = {
            "language": "en-US"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise error if request fails
        
        data = response.json()
        
        # Extract trending films
        trending_films = []
        for movie in data.get("results", [])[:5]:  # Top 5 trending
            film = {
                "title": movie.get("title", "Unknown"),
                "genre_ids": movie.get("genre_ids", []),
                "rating": movie.get("vote_average", 0),
                "popularity": movie.get("popularity", 0),
                "overview": movie.get("overview", ""),
                "release_date": movie.get("release_date", "")
            }
            trending_films.append(film)
        
        # Structure output
        output = {
            "trending_films": trending_films,
            "total_films": len(trending_films),
            "source": "TMDB Trending (Weekly)",
            "timestamp": str(data.get("dates", {}).get("max", ""))
        }
        
        return output
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trends: {e}")
        return {
            "trending_films": [],
            "error": str(e)
        }

    """
    Research global film trends from TMDB API.
    
    Returns:
        dict: Contains trending films with title, genre, rating, etc.
    """
    try:
        # TMDB endpoint for trending movies
        url = "https://api.themoviedb.org/3/trending/movie/week"
        
        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error if request fails
        
        data = response.json()
        
        # Extract trending films
        trending_films = []
        for movie in data.get("results", [])[:5]:  # Top 5 trending
            film = {
                "title": movie.get("title", "Unknown"),
                "genre_ids": movie.get("genre_ids", []),
                "rating": movie.get("vote_average", 0),
                "popularity": movie.get("popularity", 0),
                "overview": movie.get("overview", ""),
                "release_date": movie.get("release_date", "")
            }
            trending_films.append(film)
        
        # Structure output
        output = {
            "trending_films": trending_films,
            "total_films": len(trending_films),
            "source": "TMDB Trending (Weekly)",
            "timestamp": str(data.get("dates", {}).get("max", ""))
        }
        
        return output
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trends: {e}")
        return {
            "trending_films": [],
            "error": str(e)
        }
