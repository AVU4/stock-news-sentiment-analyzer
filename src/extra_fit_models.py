import numpy as np

from database_service import get_connection, get_vectorizer_from_db, \
    get_data_from_table, get_model_by_version, save_vectorizer, save_model
from util import FILES, VECTORIZERS, MODELS, get_and_increment_version
import os
import pickle


def extra_fit_vectorizer(connection, version, vectorizer_name, extra_train_X):
    filename = FILES.VECTORIZER_FILE.value
    get_vectorizer_from_db(connection, vectorizer_name, filename, version)
    with open(filename, "rb") as file:
         vectorizer = pickle.load(file)
    os.remove(filename)

    extra_train_X = vectorizer.fit_transform(extra_train_X)

    filename = FILES.VECTORIZER_FILE.value
    with open(filename, "wb") as file:
        pickle.dump(vectorizer, file)
    save_vectorizer(connection, VECTORIZERS.TF_IDF.value, filename, version + 1)
    os.remove(filename)
    return extra_train_X


def extra_fit_models(connection, version, model_name, test_x, test_y):
    filename = FILES.MODEL_FILE.value
    get_model_by_version(connection, model_name, filename, version)
    with open(filename, "rb") as file:
        model = pickle.load(file)
    os.remove(filename)
    model.fit(test_x, test_y)
    with open(filename, "wb") as file:
        pickle.dump(model, file)
    save_model(connection, model_name, filename, version + 1)
    os.remove(filename)


if __name__ == "__main__":
    connection = get_connection()
    version = get_and_increment_version()
    extra_data = get_data_from_table(connection, "DATASET_EXTRA_TRAIN")
    data = get_data_from_table(connection, "DATASET_TRAIN")
    extra_train_X = extra_fit_vectorizer(connection, version, VECTORIZERS.TF_IDF.value, np.concat(data[2], extra_data[2]))
    for model in MODELS:
        extra_fit_models(connection, version, model.value, extra_train_X, np.concat(data[1], extra_data[1]))
    connection.close()