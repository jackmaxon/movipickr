import sqlite3
from platform_data import PLATFORM_STANDARDIZATION, POPULAR_PLATFORMS
# this program is just for database manipulation and making (possibly complex) queries 

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

def standardize_platforms():
    # Connect to the database
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    # Fetch all movie records
    cursor.execute("SELECT id, platforms FROM movies")
    rows = cursor.fetchall()

    for row in rows:
        movie_id, platforms = row

        if platforms:  # Ensure the field is not NULL
            # Split the comma-separated platforms, standardize them, and join back
            platform_list = [platform.strip() for platform in platforms.split(",")]
            standardized_list = [
                PLATFORM_STANDARDIZATION.get(platform, platform) for platform in platform_list
            ]
            standardized_platforms = ", ".join(sorted(set(standardized_list)))  # Remove duplicates and sort

            # Update the database with standardized platforms
            cursor.execute(
                "UPDATE movies SET platforms = ? WHERE id = ?",
                (standardized_platforms, movie_id)
            )

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Platform standardization complete.")

def main():
    
    standardize_platforms()
    get_unique_providers()

if __name__ == "__main__":
    main()