import sqlite3
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

PLATFORM_STANDARDIZATION = {
    "A&E Crime Central Apple TV Channel": "A&E Crime Central",
    "ALLBLK": "ALLBLK",
    "ALLBLK Amazon channel": "ALLBLK",
    "ALLBLK Apple TV channel": "ALLBLK",
    "AMC": "AMC",
    "AMC Plus Apple TV Channel": "AMC+",
    "AMC+": "AMC+",
    "AMC+ Amazon Channel": "AMC+",
    "AMC+ Roku Premium Channel": "AMC+",
    "ARROW": "ARROW",
    "Acorn TV": "Acorn TV",
    "Acorn TV Apple TV": "Acorn TV",
    "AcornTV Amazon Channel": "Acorn TV",
    "Apple TV Plus": "Apple TV+",
    "Apple TV Plus Amazon Channel": "Apple TV+",
    "AsianCrush": "AsianCrush",
    "BBC America": "BBC America",
    "BET+  Apple TV channel": "BET+",
    "Bet+": "BET+",
    "Bet+ Amazon Channel": "BET+",
    "BritBox": "BritBox",
    "BritBox Amazon Channel": "BritBox",
    "Britbox Apple TV Channel": "BritBox",
    "Chai Flicks": "Chai Flicks",
    "Cinemax Amazon Channel": "Cinemax",
    "Cinemax Apple TV Channel": "Cinemax",
    "Cineverse": "Cineverse",
    "Cohen Media Amazon Channel": "Cohen Media",
    "Criterion Channel": "Criterion Channel",
    "Crunchyroll": "Crunchyroll",
    "Crunchyroll Amazon Channel": "Crunchyroll",
    "Cultpix": "Cultpix",
    "Dekkoo": "Dekkoo",
    "Disney+": "Disney+",
    "DisneyNOW": "DisneyNOW",
    "Epix Amazon Channel": "Epix",
    "Eros Now Select Apple TV Channel": "Eros Now Select",
    "FXNow": "FXNow",
    "Fandor": "Fandor",
    "Fandor Amazon Channel": "Fandor",
    "Film Movement Plus": "Film Movement Plus",
    "FilmBox+": "FilmBox+",
    "Flix Premiere": "Flix Premiere",
    "FlixFling": "FlixFling",
    "Freeform": "Freeform",
    "Full Moon Amazon Channel": "Full Moon",
    "GuideDoc": "GuideDoc",
    "HBO Max": "HBO Max",
    "Hallmark Movies Now Amazon Channel": "Hallmark Movies Now",
    "Hallmark Movies Now Apple TV Channel": "Hallmark Movies Now",
    "Hi-YAH": "Hi-YAH",
    "HiDive": "HiDive",
    "History Vault": "History Vault",
    "Hoichoi": "Hoichoi",
    "Hoopla": "Hoopla",
    "Hulu": "Hulu",
    "IFC Films Unlimited Apple TV Channel": "IFC Films Unlimited",
    "IndieFlix": "IndieFlix",
    "Kanopy": "Kanopy",
    "Kino Film Collection": "Kino Film Collection",
    "Klassiki": "Klassiki",
    "Kocowa": "Kocowa",
    "Lifetime Movie Club": "Lifetime Movie Club",
    "Lifetime Movie Club Amazon Channel": "Lifetime Movie Club",
    "Lifetime Movie Club Apple TV Channel": "Lifetime Movie Club",
    "MGM Plus": "MGM+",
    "MGM Plus Roku Premium Channel": "MGM+",
    "MUBI": "MUBI",
    "MUBI Amazon Channel": "MUBI",
    "MZ Choice Amazon Channel": "MZ Choice",
    "Max": "HBO Max",
    "Metrograph": "Metrograph",
    "Midnight Pulp": "Midnight Pulp",
    "NBC": "NBC",
    "Netflix": "Netflix",
    "Netflix Kids": "Netflix",
    "Night Flight Plus": "Night Flight Plus",
    "OVID": "OVID",
    "OnDemandKorea": "OnDemandKorea",
    "Paramount Plus": "Paramount+",
    "Paramount Plus Apple TV Channel": "Paramount+",
    "Paramount+ Amazon Channel": "Paramount+",
    "Paramount+ Roku Premium Channel": "Paramount+",
    "Paramount+ with Showtime": "Paramount+",
    "Peacock Premium": "Peacock",
    "Peacock Premium Plus": "Peacock",
    "Prime Video": "Prime Video",
    "Pure Flix": "Pure Flix",
    "Rakuten Viki": "Rakuten Viki",
    "Retrocrush": "Retrocrush",
    "Screambox": "Screambox",
    "Screambox Amazon Channel": "Screambox",
    "ScreenPix Apple TV Channel": "ScreenPix",
    "Shahid VIP": "Shahid VIP",
    "Shudder": "Shudder",
    "Shudder Amazon Channel": "Shudder",
    "Shudder Apple TV Channel": "Shudder",
    "Spectrum On Demand": "Spectrum On Demand",
    "Starz": "Starz",
    "Starz Amazon Channel": "Starz",
    "Starz Apple TV Channel": "Starz",
    "Starz Roku Premium Channel": "Starz",
    "Strand Releasing Amazon Channel": "Strand Releasing",
    "Sun Nxt": "Sun Nxt",
    "Sundance Now": "Sundance Now",
    "TBS": "TBS",
    "TCM": "TCM",
    "TNT": "TNT",
    "Troma NOW": "Troma NOW",
    "UP Faith & Family Apple TV Channel": "UP Faith & Family",
    "USA Network": "USA Network",
    "VIX": "VIX",
    "Vix Gratis Amazon Channel": "VIX",
    "aha": "aha",
    "fuboTV": "fuboTV",
    "iQIYI": "iQIYI",
    "tru TV": "tru TV"
}

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