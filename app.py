from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3
import random
import os
import logging

app = Flask(__name__, static_folder='static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'movies.db')

# Set up logging
logging.basicConfig(level=logging.INFO)

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
        ','.join(movie.get('platforms', [])),  
        movie['poster_url'],
        movie.get('actors', None),
        movie.get('language', None),
        movie.get('directors', None),
        movie.get('budget', None),
        movie.get('revenue', None),
        movie.get('keywords', None)
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
    return render_template('movipickr.html')  # Ensure this matches your actual file name

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

def main():
    app.run() # comment out when deploying on cPanel

if __name__ == '__main__':
    main()
