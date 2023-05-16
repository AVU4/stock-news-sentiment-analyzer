import pickle
import time
import os
from sklearn.metrics import accuracy_score
from database_service import get_connection, get_vectorizer_by_version, get_data_from_table, get_model_by_version


def get_vectorizer(connection, version):
    filename = "../resources/vectorizer.txt"
    get_vectorizer_by_version(connection, "tf_idf", filename, version)
    with open(filename, "rb") as file:
         vectorizer = pickle.load(file)
    os.remove(filename)
    return vectorizer


def estimate_random_forest(connection, vectorizer, version, test_x, test_y):
    vectorized_test_x = vectorizer.transform(test_x)
    filename = "../resources/model.txt"
    get_model_by_version(connection, "random_forest", filename, version)
    with open(filename, "rb") as file:
        model = pickle.load(file)
    os.remove(filename)
    start = time.time()
    predicted_y = model.predict(vectorized_test_x)
    duration = time.time() - start
    print(accuracy_score(test_y, predicted_y))
    print(duration)
    #todo save metrics of model



def estimate_logistic_regression(connection, vectorizer, version, test_x, test_y):
    vectorized_test_x = vectorizer.transform(test_x)
    filename = "../resources/model.txt"
    get_model_by_version(connection, "logistic_regression", filename, version)
    with open(filename, "rb") as file:
        model = pickle.load(file)
    os.remove(filename)
    start = time.time()
    predicted_y = model.predict(vectorized_test_x)
    duration = time.time() - start
    print(accuracy_score(test_y, predicted_y))
    print(duration)


def get_version():
    with open("../resources/model_version.txt", "r") as file:
        return int(file.readline())


if __name__ == "__main__":
    connection = get_connection()
    version = get_version()
    data = get_data_from_table(connection, "DATASET_TEST")
    vectorizer = get_vectorizer(connection, version)
    estimate_logistic_regression(connection, vectorizer, version, data[2], data[1])
    estimate_random_forest(connection, vectorizer, version, data[2], data[1])
    connection.close()
