import pickle
import time
import os
from util import MODELS, FILES, VECTORIZERS
from sklearn.metrics import accuracy_score
from database_service import get_connection, get_vectorizer, get_data_from_table, get_model_by_version, \
    update_model_metrics
from util import get_version


def get_vectorizer(connection, version, vectorizer_name):
    filename = FILES.VECTORIZER_FILE.value
    get_vectorizer(connection, vectorizer_name, filename, version)
    with open(filename, "rb") as file:
         vectorizer = pickle.load(file)
    os.remove(filename)
    return vectorizer


def save_model(connection, vectorizer, version, model_name, test_x, test_y):
    vectorized_test_x = vectorizer.transform(test_x)
    filename = FILES.MODEL_FILE.value
    get_model_by_version(connection, model_name, filename, version)
    with open(filename, "rb") as file:
        model = pickle.load(file)
    os.remove(filename)
    start = time.time()
    predicted_y = model.predict(vectorized_test_x)
    duration = time.time() - start
    accuracy = accuracy_score(test_y, predicted_y)
    update_model_metrics(connection, model_name, version, accuracy, duration)


if __name__ == "__main__":
    connection = get_connection()
    version = get_version()
    data = get_data_from_table(connection, "DATASET_TEST")
    vectorizer = get_vectorizer(connection, version, VECTORIZERS.TF_IDF.value)
    for model in MODELS.value:
        save_model(connection, vectorizer, version, model, data[2], data[1])
    connection.close()
