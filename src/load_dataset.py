import pandas as pd
import sys
from database_service import get_connection, create_table_with_raw_data, save_data


def handle_dataset(filename):
    data = pd.read_csv(filename, delimiter='\t')
    connection = get_connection()
    create_table_with_raw_data(connection, 'DATASET_RAW')
    save_data(connection, data, 'DATASET_RAW')
    connection.close()


if __name__ == "__main__":
    handle_dataset(sys.argv[1])
