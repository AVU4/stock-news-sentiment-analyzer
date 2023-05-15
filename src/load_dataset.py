import pandas as pd
import sys


def handle_dataset(filename):
    data = pd.read_csv(filename, delimiter='\t')
    print(data)


if __name__ == "__main__":
    handle_dataset(sys.argv[1])