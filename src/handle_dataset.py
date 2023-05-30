import re
import nltk
import pymorphy2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from database_service import get_raw_data_from_table, get_connection, create_modified_table, save_modified_data


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
    data = get_raw_data_from_table(connection, "DATASET_RAW")
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    test_data, extra_train_data = train_test_split(test_data, test_size=0.5, random_state=42)

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

    extra_train_data[2] = modify_text(extra_train_data[2], morph_analyzer)
    extra_train_data[1] = extra_train_data[1].apply(lambda v: label_score(v))

    create_modified_table(connection, "DATASET_EXTRA_TRAIN")
    save_modified_data(connection, extra_train_data, "DATASET_EXTRA_TRAIN")

    connection.close()
