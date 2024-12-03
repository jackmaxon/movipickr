from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3
import random
import os
import logging

app = Flask(__name__, static_folder='static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'movies.db')

# Set up logging
logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# PLATFORM_STANDARDIZATION dictionary (used for data standardization)
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

# Define platform popularity ranking (used for ordering platforms in the UI)
POPULAR_PLATFORMS = [
    "Netflix",
    "Prime Video",
    "Disney+",
    "HBO Max",
    "Hulu",
    "Apple TV+",
    "Paramount+",
    "Peacock",
    "Starz",
    "Showtime",
    "AMC+",
    "MUBI",
    "Crunchyroll",
    "Acorn TV",
    "Shudder",
    "Sundance Now",
    "BritBox",
    "Kanopy",
    "Hoopla",
    "Criterion Channel",
    "Epix",
    "Cinemax",
    "Hallmark Movies Now",
    "BET+",
    "History Vault",
    "fuboTV",
    "Tubi",
    "Max",  # HBO Max may also be referred to as Max
    "BBC America",
    "FXNow",
    "NBC",
    "Spectrum On Demand",
    "Rakuten Viki",
    "Midnight Pulp",
    "IndieFlix",
    "Dekkoo",
    "AsianCrush",
    "Hi-YAH",
    "Retrocrush",
    "Shahid VIP",
    "iQIYI",
    "Night Flight Plus",
    "MZ Choice",
    "Fandor",
    "Film Movement Plus",
    "Full Moon",
    "Metrograph",
    "MGM+",
    "ARROW",
    "ALLBLK",
    "A&E Crime Central",
    "Chai Flicks",
    "Cohen Media",
    "Cultpix",
    "Eros Now Select",
    "FilmBox+",
    "Flix Premiere",
    "FlixFling",
    "GuideDoc",
    "Hoichoi",
    "IFC Films Unlimited",
    "Kino Film Collection",
    "Klassiki",
    "Kocowa",
    "Lifetime Movie Club",
    "OnDemandKorea",
    "OVID",
    "Pure Flix",
    "ScreenPix",
    "Strand Releasing",
    "Sun Nxt",
    "TCM",
    "TBS",
    "TNT",
    "Troma NOW",
    "UP Faith & Family",
    "USA Network",
    "VIX",
    "aha",
    "tru TV"
]

# Combine with any remaining platforms not already in POPULAR_PLATFORMS
remaining_platforms = [
    platform for platform in sorted(set(PLATFORM_STANDARDIZATION.values()))
    if platform not in POPULAR_PLATFORMS
]

# Final ordered list of platforms to be displayed
PLATFORMS_LIST = POPULAR_PLATFORMS + remaining_platforms

def create_database():
    conn = sqlite3.connect(DATABASE_PATH)
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
    conn = sqlite3.connect(DATABASE_PATH)
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
        movie.get('stars', None),  
        ', '.join(movie.get('platforms', [])),  
        movie['poster_url'],
        ', '.join(movie.get('actors', [])),
        movie.get('language', None),
        ', '.join(movie.get('directors', [])),
        movie.get('budget', 0),
        movie.get('revenue', 0),
        ', '.join(movie.get('keywords', []))
    ))

    conn.commit()
    conn.close()

def get_random_movie(platforms):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    platforms = [platform.lower() for platform in platforms]
    query = "SELECT * FROM movies WHERE " + " OR ".join(["LOWER(platforms) LIKE ?"] * len(platforms))
    platform_filters = [f"%{platform.strip()}%" for platform in platforms]
    
    cursor.execute(query, platform_filters)
    movies = cursor.fetchall()
    
    conn.close()
    
    if not movies:
        return None
    
    # Randomly select a movie and format it as a dictionary
    columns = [col[0] for col in cursor.description]
    random_movie = dict(zip(columns, random.choice(movies)))
    return random_movie

@app.route('/')
def home():
    return render_template('movipickr.html', platforms=PLATFORMS_LIST)

@app.route('/select-platforms', methods=['POST'])
def select_platforms():
    platforms = request.form.getlist('platforms')
    if not platforms:
        return "Please select at least one platform.", 400
    return redirect(url_for('random_movie', platforms=",".join(platforms)))

@app.route('/movie/random', methods=['GET'])
def random_movie():
    platforms = request.args.get('platforms', '').split(',')
    if not platforms:
        return jsonify({'error': 'No platforms specified'}), 400

    # Log the incoming platforms for debugging
    logging.info(f"Platforms received: {platforms}")

    # Build the query dynamically based on selected platforms
    query = "SELECT * FROM movies WHERE " + " OR ".join(["LOWER(platforms) LIKE ?"] * len(platforms))
    params = [f"%{platform.lower()}%" for platform in platforms]

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    movies = cursor.fetchall()

    if not movies:
        logging.info("No movies found for the selected platforms.")
        return jsonify({'error': 'No movies available for the selected platforms!'}), 404

    # Randomly select a movie and format it as a dictionary
    columns = [col[0] for col in cursor.description]
    random_movie = dict(zip(columns, random.choice(movies)))

    conn.close()
    return jsonify(random_movie)

# Initialize the database if it doesn't exist
if not os.path.exists(DATABASE_PATH):
    create_database()
    # Optionally, populate your database here with insert_movie()

# Ensure the app runs only when executed directly
if __name__ == '__main__':
    app.run(debug=False)
