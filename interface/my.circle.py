from flask import Flask, render_template
import data_analyser

app = Flask(__name__)


@app.route('/data/<int:year>-<int:month>-<int:day>')
def get_data(year, month, day):
    data = data_analyser.get_data_csv(year, month, day)
    return data
    # return render_template("data.txt")


@app.route('/')
def index():
    records = data_analyser.get_records("2014-09-22", "2014-11-17")
    size_records = sorted(records, key=lambda row: row['radius'], reverse=True)
    return render_template("index.html", records=records, size_records=size_records)


if __name__ == '__main__':
    app.run(debug=True)
