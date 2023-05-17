import pickle
import os
from util import MODELS, FILES, VECTORIZERS
from database_service import get_connection
from sklearn.feature_extraction.text import TfidfVectorizer
from database_service import get_data_from_table, save_model, save_vectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from util import get_and_increment_version


def fit_tf_idf_vectorizer(connection, model_version):
    tf_idf_vectorizer = TfidfVectorizer()
    train_data = get_data_from_table(connection, "DATASET_TRAIN")
    train_x = tf_idf_vectorizer.fit_transform(train_data[2])

    filename = FILES.VECTORIZER_FILE.value
    with open(filename, "wb") as file:
        pickle.dump(tf_idf_vectorizer, file)
    save_vectorizer(connection, VECTORIZERS.TF_IDF.value, filename, model_version)
    os.remove(filename)

    return train_x, train_data[1]


def fit_logistic_regression_model(connection, model_version, train_x, train_y):
    model = LogisticRegression(random_state=100)
    model.fit(train_x, train_y)
    filename = FILES.MODEL_FILE.value
    with open(filename, "wb") as file:
        pickle.dump(model, file)
    save_model(connection, MODELS.LOGISTIC_REGRESSION.value, filename, model_version)
    os.remove(filename)


def fit_random_forest_classifier(connection, model_version, train_x, train_y):
    model = RandomForestClassifier(random_state=100)
    model.fit(train_x, train_y)
    filename = FILES.MODEL_FILE.value
    with open(filename, "wb") as file:
        pickle.dump(model, file)
    save_model(connection, MODELS.RANDOM_FOREST.value, filename, model_version)
    os.remove(filename)


if __name__ == "__main__":
    connection = get_connection()
    current_version = get_and_increment_version()
    train_x, train_y = fit_tf_idf_vectorizer(connection, current_version)
    fit_logistic_regression_model(connection, current_version, train_x, train_y)
    fit_random_forest_classifier(connection, current_version, train_x, train_y)
    connection.close()
