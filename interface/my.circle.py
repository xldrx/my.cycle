from flask import Flask, render_template
from interface import data_analyser

app = Flask(__name__)


@app.route('/data/<int:year>-<int:month>-<int:day>')
def get_data(year, month, day):
    data = data_analyser.get_data_csv(year, month, day)
    return data
    # return render_template("data.txt")


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
