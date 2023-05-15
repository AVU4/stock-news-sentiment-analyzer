import psycopg2
import os
from psycopg2 import sql


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="aii",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD")
    )

def create_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(sql.SQL(
        "CREATE TABLE {table} ("
        "id int primary key, "
        "title text, "
        "score double precision, "
        "link text,"
        "summary text, "
        "published timestamp,"
        "tickers text[]);").format(table=sql.Identifier(table_name)))
    cursor.close()
    connection.commit()
