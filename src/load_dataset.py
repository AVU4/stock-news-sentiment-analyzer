import pandas as pd
import sys
import psycopg2
from psycopg2 import sql


def handle_dataset(filename):
    data = pd.read_csv(filename, delimiter='\t')
    connection = psycopg2.connect(
        host="127.0.0.1:5432",
        database="postgres",
        user="postgres",
        password="test"
    )
    cursor = connection.cursor()
    cursor.execute(sql.SQL("CREATE TABLE TEST;"))
    cursor.close()
    connection.close()
    print(data)


if __name__ == "__main__":
    handle_dataset(sys.argv[1])