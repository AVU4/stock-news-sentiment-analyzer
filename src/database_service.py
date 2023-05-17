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


def get_model_metrics(connection, current_version):
    cursor = connection.cursor()
    cursor.execute(sql.SQL("select name, accuracy, time from model where version=%s"), [current_version])
    result = DataFrame(cursor.fetchall(), index=None)
    cursor.close()
    return result

def update_model_metrics(connection, model_name, current_version, accuracy_score, duration):
    cursor = connection.cursor()
    cursor.execute(sql.SQL("update model set accuracy=%s, time=%s where name=%s and version=%s"), (accuracy_score, duration, model_name, current_version))
    cursor.close()
    connection.commit()


def get_model_by_version(connection, model_name, filename, current_version):
    cursor = connection.cursor()
    cursor.execute(sql.SQL("SELECT model_data from model where version=%s and name=%s"), (current_version, model_name))
    model_data = cursor.fetchone()[0]
    with open(filename, "wb") as file:
        file.write(model_data)
    cursor.close()


def get_vectorizer_by_version(connection, vectorizer_name, filename, current_version):
    cursor = connection.cursor()
    cursor.execute(sql.SQL("SELECT vectorizer_data from vectorizer where version=%s and name=%s"), (current_version, vectorizer_name))
    vectorizer_data = cursor.fetchone()[0]
    with open(filename, "wb") as file:
        file.write(vectorizer_data)
    cursor.close()

def save_vectorizer(connection, vectorizer_name, filename, current_version):
    cursor = connection.cursor()
    with open(filename, "rb") as file:
        cursor.execute(sql.SQL("INSERT INTO vectorizer (name, vectorizer_data, version) VALUES (%s, %s, %s)"),
                       (vectorizer_name, psycopg2.Binary(file.read()), current_version))
    cursor.close()
    connection.commit()


def save_model(connection, model_name, filename, current_model_version):
    cursor = connection.cursor()
    with open(filename, "rb") as file:
        cursor.execute(sql.SQL("INSERT INTO model (name, model_data, version) VALUES (%s, %s, %s)"),
                       (model_name, psycopg2.Binary(file.read()), current_model_version))
    cursor.close()
    connection.commit()


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


def get_raw_data_from_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(sql.SQL("select id, score, summary from {table}").format(table=sql.Identifier(table_name)))
    result = DataFrame(cursor.fetchall(), index=None)
    result.set_index(0, inplace=True)
    cursor.close()
    return result


def get_data_from_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(sql.SQL("select * from {table}").format(table=sql.Identifier(table_name)))
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


def save_best_model(connection, version, name, score):
    cursor = connection.cursor()
    cursor.execute(sql.SQL("INSERT INTO best_model (version, name, score) values (%s, %s, %s)"), (version, name, score))
    cursor.close()
    connection.commit()

