import psycopg2
import os
from psycopg2 import sql
from pandas import DataFrame


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="aii",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD")
    )


def drop_table(cursor, table_name):
    cursor.execute(sql.SQL("DROP TABLE {table};").format(table=sql.Identifier(table_name)))


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


def save_data(connection, data, table_name):
    cursor = connection.cursor()
    for index, row in data.iterrows():
        cursor.execute(sql.SQL("INSERT INTO {table}(id, title, score, link, summary, published, tickers) values (%s, %s, %s, %s, %s, %s, %s)")
                       .format(table=sql.Identifier(table_name)),
                       (index, row['title'], row['score'], row['link'], row['summary'], row['published'], row['tickers'].replace('[', '{').replace(']', '}')))
    cursor.close()
    connection.commit()


def get_data_from_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(sql.SQL("select id, score, summary from {table}").format(table=sql.Identifier(table_name)))
    result = DataFrame(cursor.fetchall(), index=None)
    result.set_index(0, inplace=True)
    cursor.close()
    return result


def create_modified_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(sql.SQL("CREATE TABLE {table} (id integer primary key, score double precision, summary text)").format(table=sql.Identifier(table_name)))
    cursor.close()
    connection.commit()


def save_modified_data(connection, data, table_name):
    cursor = connection.cursor()
    for index, row in data.iterrows():
        cursor.execute(sql.SQL("INSERT INTO {table} (id, score, summary) values(%s, %s, %s)").format(table=sql.Identifier(table_name)), (index, row[1], row[2]))
    cursor.close()
    connection.commit()

