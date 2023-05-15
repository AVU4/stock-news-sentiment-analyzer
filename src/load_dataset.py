import pandas as pd
import sys
from database_service import get_connection, create_table


def handle_dataset(filename):
    data = pd.read_csv(filename, delimiter='\t')
    connection = get_connection()
    create_table(connection, 'DATASET_RAW')
    connection.close()
    print(data)


if __name__ == "__main__":
    handle_dataset(sys.argv[1])
