import mariadb

conn = mariadb.connect(
    host="127.0.0.1",
    port="3007",
    user="py",
    password="esonero",
    database="movies_db"
)

def execute_query(connection: mariadb.Connection, query: str):
    cursor: mariadb.Cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    connection.commit()

    cursor.close()
    return results