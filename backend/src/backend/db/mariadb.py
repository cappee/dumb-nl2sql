import csv
import mariadb

from backend.endpoints.add.models import Data


def db_connection():
    """Return a connection to the database, and close it when done"""
    conn = mariadb.connect(
        host="database",
        port=3306,
        user="py",
        password="esonero",
        database="movies_db"
    )
    try:
        yield conn
    finally:
        conn.close()


def execute_query(connection: mariadb.Connection, query: str):
    """Execute a query and return the results"""
    cursor: mariadb.Cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    connection.commit()

    cursor.close()
    return results


def insert_data(connection: mariadb.Connection, data: Data) -> bool:
    """Insert (or update) data into the database"""
    try:
        cursor = connection.cursor()

        # Insert (or update data if alredy exists) director
        cursor.execute("""
            INSERT INTO directors (name, age)
            VALUES (?, ?)
            ON DUPLICATE KEY UPDATE
                age = VALUES(age)
        """, (data.director, data.director_age))

        # Search for director ID
        cursor.execute("SELECT director_id FROM directors WHERE name = ?", (data.director,))
        director_id = cursor.fetchone()[0]

        # Insert (or update data if already exists) movie
        cursor.execute("""
            INSERT INTO movies (name, release_year, genre, director_id)
            VALUES (?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE
                release_year = VALUES(release_year),
                genre = VALUES(genre),
                director_id = VALUES(director_id)
        """, (data.name, data.release_year, data.genre, director_id))

        # Search for movie ID
        cursor.execute("SELECT movie_id FROM movies WHERE name = ?", (data.name,))
        movie_id = cursor.fetchone()[0]

        # Delete all link between this movie and platforms
        cursor.execute("DELETE FROM watch_on WHERE movie_id = ?", (movie_id,))

        for platform in [data.platform1, data.platform2]:
            # Check if platform is null
            if not platform or not platform.strip():
                continue

            # Insert (or ignore if alredy exists) platform
            cursor.execute("""
                INSERT IGNORE INTO platforms (name)
                VALUES (?)
            """, (platform,))

            # Search for platform ID
            cursor.execute("SELECT platform_id FROM platforms WHERE name = ?", (platform,))
            platform_id = cursor.fetchone()[0]

            # Insert link between movie and platform
            cursor.execute(
                "INSERT INTO watch_on (movie_id, platform_id) VALUES (?, ?)",
                (movie_id, platform_id)
            )
            
        """Commit the transaction"""
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    

def is_empty(connection: mariadb.Connection) -> bool:
    """Return True if the database is empty, False otherwise"""
    if execute_query(connection, "SELECT COUNT(*) FROM movies")[0][0] == 0:
        return True
    return False


def populate_if_empty(connection: mariadb.Connection):
    """Populate the database with initial data from a given file, if it's empty"""
    if not is_empty(connection):
        return
    
    with open("backend/data.tsv", encoding="utf-8") as file:
        # Read the TSV file as a dictionary because Pydantic use dicts
        # to validate the data; the delimiter is set to tab to match the TSV format
        tsv = csv.DictReader(file, delimiter="\t")
        data = [Data.model_validate(row) for row in tsv]

        for movie in data:
            # Insert each movie into the database
            insert_data(connection, movie)
    
