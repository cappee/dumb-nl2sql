from fastapi import HTTPException
import mariadb

from backend.endpoints.add.models import Data


def db_connection():
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
    cursor: mariadb.Cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    connection.commit()

    cursor.close()
    return results


def insert_data(connection: mariadb.Connection, data: Data) -> bool:
    try:
        cursor = connection.cursor()
        
        """Search for director in db, if not found, insert it"""
        cursor.execute(
            "SELECT director_id FROM directors WHERE name = ?", 
            (data.director,))
        row = cursor.fetchone()

        if row:
            director_id = row[0]
        else:
            cursor.execute("INSERT IGNORE INTO directors (name, age) VALUES (?, ?)", 
                        (data.director, data.director_age))
            director_id = cursor.lastrowid

        """Insert movie into db"""
        cursor.execute("INSERT IGNORE INTO movies (name, release_year, genre, director_id) VALUES (?, ?, ?, ?)",
                    (data.name, data.release_year, data.genre, director_id))
        movie_id = cursor.lastrowid

        """Search for platforms in db, if not found, insert them and create a relation with the movie"""
        for platform in [data.platform1, data.platform2]:
            cursor.execute("SELECT platform_id FROM platforms WHERE name = ?", 
                        (platform,))
            row = cursor.fetchone()
            if row:
                platform_id = row[0]
            else:
                cursor.execute("INSERT IGNORE INTO platforms (name) VALUES (?)", 
                            (platform,))
                platform_id = cursor.lastrowid

            cursor.execute("INSERT IGNORE INTO watch_on (movie_id, platform_id) VALUES (?, ?)",
                        (movie_id, platform_id))
            
        """Commit the transaction"""
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error inserting data into database: {str(e)}"
        )