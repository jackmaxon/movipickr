import sqlite3
# this program is just for database manipulation and making queries 

def get_unique_providers():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    cursor.execute("SELECT platforms FROM movies")
    rows = cursor.fetchall()

    unique_platforms = set()

    for row in rows:
        if row[0]:  # Ensure the row is not empty or NULL
            platforms = [platform.strip() for platform in row[0].split(",")]  # Split and strip whitespace
            unique_platforms.update(platforms)  # Add to the set

    for platform in sorted(unique_platforms):
        print(platform)

    conn.close()

def get_popular_platforms():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    # Split platforms and count occurrences
    query = """
    SELECT platform, COUNT(*) as count FROM (
        SELECT TRIM(platform) as platform FROM (
            SELECT DISTINCT TRIM(value) as platform
            FROM movies, json_each('[' || REPLACE(platforms, ',', '","') || ']')
        )
    ) GROUP BY platform ORDER BY count DESC;
    """
    cursor.execute(query)
    platforms = cursor.fetchall()
    conn.close()

    return platforms