from fastapi import HTTPException
import mariadb

from backend.models.models import Data, TableSchema


def db_connection() -> mariadb.Connection:
    try:
        conn = mariadb.connect(
            host="database",
            port=3306,
            user="py",
            password="esonero",
            database="movies_db"
        )
        return conn
    except mariadb.Error as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error during MariaDB connection: {str(e)}"
        )


def execute_query(connection: mariadb.Connection, query: str):
    cursor: mariadb.Cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    connection.commit()

    cursor.close()
    return results


def get_schema(connection: mariadb.Connection) -> list[TableSchema]:
    schema: list[TableSchema] = list()

    tables = execute_query(connection, "SHOW tables;")
    for table in tables:
        columns = execute_query(connection, f"SHOW columns FROM {table[0]}")
        for column in columns:
            schema.append(TableSchema(table_name=table[0], table_column=column[0]))

    return schema


def add_data_to_db(connection: mariadb.Connection, data: Data) -> bool:
    try:
        cursor = connection.cursor()
        
        """Search for director in db, if not found, insert it"""
        cursor.execute(
            "SELECT director_id FROM directors WHERE name = ? AND age = ?", 
            (data.director, data.director_age))
        row = cursor.fetchone()

        if row:
            director_id = row[0]
        else:
            cursor.execute("INSERT INTO directors (name, age) VALUES (?, ?)", 
                        (data.director, data.director_age))
            director_id = cursor.lastrowid

        """Insert movie into db"""
        cursor.execute("INSERT INTO movies (title, release_year, genre, director_id) VALUES (?, ?, ?, ?)",
                    (data.title, data.release_year, data.genre, director_id))
        movie_id = cursor.lastrowid

        """Search for platforms in db, if not found, insert them and create a relation with the movie"""
        for platform in [data.platform1, data.platform2]:
            cursor.execute("SELECT platform_id FROM platforms WHERE name = ?", 
                        (platform,))
            row = cursor.fetchone()
            if row:
                platform_id = row[0]
            else:
                cursor.execute("INSERT INTO platforms (name) VALUES (?)", 
                            (platform,))
                platform_id = cursor.lastrowid

            cursor.execute("INSERT INTO watch_on (movie_id, platform_id) VALUES (?, ?)",
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