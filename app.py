from flask import Flask, render_template, request, jsonify
import joblib
from src.database_service import get_connection, get_best_model, get_best_vectorizer
from src.util import FILES

app = Flask(__name__)
connection = get_connection()
filename_model = FILES.MODEL_FILE.value
get_best_model(connection, filename_model)
model = joblib.load(filename_model)
filename_vectorizer = FILES.VECTORIZER_FILE.value
get_best_vectorizer(connection, filename_vectorizer)
vectorizer = joblib.load(filename_vectorizer)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/news', methods=['POST'])
def analysis_news():
    req = request.get_json()
    news = req['data']
    print(news)
    vectorized_news = vectorizer.transform([news])
    score = str(model.predict(vectorized_news)[0])
    print(score)
    data = {'score' : score}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
    connection.close()
