from database_service import get_connection, get_model_metrics, save_best_model
from util import get_version


class Model:
    def __init__(self, name, score):
        self.name = name
        self.score = score


def select_model(connection, version):
    model_metrics = get_model_metrics(connection, version)
    result = []
    for index, row in model_metrics.iterrows():
        score = 1/row[1] + row[2]
        result.append(Model(row[0], score))
    result.sort(key=lambda x: x.score)
    save_best_model(connection, version, result[0].name, result[0].score)


if __name__ == "__main__":
    connection = get_connection()
    version = get_version()
    select_model(connection, version)
    connection.close()
