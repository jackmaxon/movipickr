import sqlite3
from platform_data import PLATFORM_STANDARDIZATION, POPULAR_PLATFORMS
import requests
from dotenv import load_dotenv
import os
from datetime import datetime


def create_database():
    conn = sqlite3.connect('movies.db')  
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        title TEXT,
        release_date TEXT,
        overview TEXT,
        genres TEXT,
        runtime INTEGER,
        stars TEXT,
        platforms TEXT,
        poster_url TEXT,
        actors TEXT,
        language TEXT,
        directors TEXT,
        budget INTEGER,
        revenue INTEGER,
        keywords TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_movie(movie):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO movies (
        id, title, release_date, overview, genres, runtime, stars, platforms, 
        poster_url, actors, language, directors, budget, revenue, keywords
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        movie['id'],
        movie['title'],
        movie['release_date'],
        movie['overview'],
        movie['genres'],
        movie.get('runtime', None),
        movie.get('stars'),
        ', '.join(movie.get('platforms', [])),
        movie['poster_url'],
        ', '.join(movie.get('actors', [])),
        movie['language'],
        ', '.join(movie.get('directors', [])),
        movie.get('budget', 0),
        movie.get('revenue', 0),
        ', '.join(movie.get('keywords', []))
    ))
    conn.commit()
    conn.close()

def fetch_movie_details(api_key, movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching movie details for ID {movie_id}: {response.status_code}")
        return {}

def fetch_movie_credits(api_key, movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching credits for movie ID {movie_id}: {response.status_code}")
        return {}

def fetch_movie_keywords(api_key, movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('keywords', [])
    else:
        print(f"Error fetching keywords for movie ID {movie_id}: {response.status_code}")
        return []

def fetch_streaming_providers(api_key, movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        providers = response.json().get('results', {}).get('US', {}).get('flatrate', [])
        return [provider['provider_name'] for provider in providers if 'provider_name' in provider]
    else:
        print(f"Error fetching providers for movie ID {movie_id}: {response.status_code}")
        return []

def standardize_platforms(providers):
    standardized = set()
    for platform in providers:
        # Strip whitespace and standardize casing
        platform_cleaned = platform.strip()
        # Standardize platform name
        standardized_name = PLATFORM_STANDARDIZATION.get(platform_cleaned, platform_cleaned)
        standardized.add(standardized_name)
    return list(standardized)

def fetch_popular_movies(api_key, page=1):
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&page={page}'
    response = requests.get(url)

    if response.status_code == 200:
        movies = response.json()['results']   
        structured_movies = []
        for movie in movies:
            movie_id = movie.get("id")
            if not movie_id:
                print(f"Skipping movie without an ID: {movie}")
                continue

            # Fetch additional details
            movie_details = fetch_movie_details(api_key, movie_id)
            credits = fetch_movie_credits(api_key, movie_id)
            keywords_data = fetch_movie_keywords(api_key, movie_id)
            streaming_providers = fetch_streaming_providers(api_key, movie_id)

            runtime = movie_details.get("runtime")
            language = movie_details.get("original_language")
            budget = movie_details.get("budget", 0)
            revenue = movie_details.get("revenue", 0)

            actors = [member['name'] for member in credits.get('cast', [])[:5]]  # Top 5 actors
            directors = [member['name'] for member in credits.get('crew', []) if member['job'] == "Director"]

            keywords = [keyword['name'] for keyword in keywords_data]

            platforms = standardize_platforms(streaming_providers)

            poster_path = movie.get('poster_path')
            poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}' if poster_path else None

            genres = ', '.join([genre['name'] for genre in movie_details.get('genres', [])])
            vote_average = movie.get("vote_average", 0)
            stars = f"{round(vote_average * 2) / 2} Stars"

            structured_movies.append({
                "id": movie_id,
                "title": movie.get("title"),
                "release_date": format_date(movie.get("release_date")),
                "overview": movie.get("overview"),
                "genres": genres,
                "runtime": runtime,
                "stars": stars,
                "platforms": platforms,
                "poster_url": poster_url,
                "actors": actors,
                "language": language,
                "directors": directors,
                "budget": budget,
                "revenue": revenue,
                "keywords": keywords
            })

        return structured_movies
    else:
        print(f"Error: {response.status_code}")
        return []

def format_date(release_date):
    if not release_date:
        return "Unknown"
    try:
        date_obj = datetime.strptime(release_date, '%Y-%m-%d')
        return date_obj.strftime('%B %Y')
    except ValueError:
        return "Unknown"

def main():
    load_dotenv()
    api_key = os.getenv('api_key')

    create_database()

    total_pages = 500
    for page in range(1, total_pages + 1):
        print(f"Fetching page {page}")
        movies = fetch_popular_movies(api_key, page=page)
        for movie in movies:
            insert_movie(movie)

if __name__ == "__main__":
    main()