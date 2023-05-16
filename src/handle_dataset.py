from database_service import get_data_from_table, get_connection, save_data, create_modified_table, save_modified_data
from sklearn.model_selection import train_test_split
import nltk
import pickle
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy2
from sklearn.feature_extraction.text import TfidfVectorizer


def modify_text(text, morph):
    modified = []
    for row in text:
        row = re.sub(r'[^\w\s]', '', str(row).lower().strip())
        tokens = word_tokenize(row)
        modified.append(" ".join([morph.normal_forms(word)[0] for word in tokens if not word in stopwords.words('russian')]))
    return modified


def label_score(score):
    if score > 0:
        return 1
    else:
        return -1


if __name__ == "__main__":
    connection = get_connection()
    data = get_data_from_table(connection, "DATASET_RAW")
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

    morph_analyzer = pymorphy2.MorphAnalyzer()
    nltk.download('stopwords')
    nltk.download('punkt')

    train_data[2] = modify_text(train_data[2], morph_analyzer)
    train_data[1] = train_data[1].apply(lambda v: label_score(v))

    create_modified_table(connection, "DATASET_TRAIN")
    save_modified_data(connection, train_data, "DATASET_TRAIN")

    test_data[2] = modify_text(test_data[2], morph_analyzer)
    test_data[1] = test_data[1].apply(lambda v: label_score(v))

    create_modified_table(connection, "DATASET_TEST")
    save_modified_data(connection, test_data, "DATASET_TEST")

    connection.close()
