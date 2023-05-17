import enum


class MODELS(enum.Enum):
    LOGISTIC_REGRESSION = "logistic_regression",
    RANDOM_FOREST = "random_forest"


class VECTORIZERS(enum.Enum):
    TF_IDF = "tf_idf"


class FILES(enum.Enum):
    MODEL_FILE = "resources/model.txt"
    VECTORIZER_FILE = "resources/vectorizer.txt"


def get_and_increment_version():
    with open("resources/model_version.txt", "r+") as file:
        version = int(file.readline(1)) + 1
        file.seek(0)
        file.write(str(version))
        file.truncate()
        return version


def get_version():
    with open("resources/model_version.txt", "r") as file:
        return int(file.readline(1)) + 1