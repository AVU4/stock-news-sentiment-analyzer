import pickle
import os
from database_service import get_connection
from sklearn.feature_extraction.text import TfidfVectorizer
from database_service import get_data_from_table, save_model, save_vectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


def fit_vectorizer(connection, model_version):
    tf_idf_vectorizer = TfidfVectorizer()
    train_data = get_data_from_table(connection, "DATASET_TRAIN")
    train_x = tf_idf_vectorizer.fit_transform(train_data[2])

    filename = "resources/vectorizer.txt"
    with open(filename, "wb") as file:
        pickle.dump(tf_idf_vectorizer, file)
    save_vectorizer(connection, "tf_idf", filename, model_version)
    os.remove(filename)

    return train_x, train_data[1]


def fit_logistic_regression_model(connection, model_version, train_x, train_y):
    model = LogisticRegression(random_state=100)
    model.fit(train_x, train_y)
    filename = "resources/model.txt"
    with open(filename, "wb") as file:
        pickle.dump(model, file)
    save_model(connection, "logistic_regression", filename, model_version)
    os.remove(filename)


def fit_random_forest_classifier(connection, model_version, train_x, train_y):
    model = RandomForestClassifier(random_state=100)
    model.fit(train_x, train_y)
    filename = "resources/model.txt"
    with open(filename, "wb") as file:
        pickle.dump(model, file)
    save_model(connection, "random_forest", filename, model_version)
    os.remove(filename)


def get_and_update_version():
    with open("resources/model_version.txt", "r+") as file:
        version = int(file.readline(1)) + 1
        file.seek(0)
        file.write(str(version))
        file.truncate()
        return version


if __name__ == "__main__":
    connection = get_connection()
    current_version = get_and_update_version()
    train_x, train_y = fit_vectorizer(connection, current_version)
    fit_logistic_regression_model(connection, current_version, train_x, train_y)
    fit_random_forest_classifier(connection, current_version, train_x, train_y)
    connection.close()
